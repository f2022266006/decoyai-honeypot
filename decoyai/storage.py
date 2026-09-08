"""SQLite persistence and aggregate statistics."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .classifier import Classification, risk_level


SCHEMA = """
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc TEXT NOT NULL,
    source_ip TEXT NOT NULL,
    source_port INTEGER NOT NULL,
    service TEXT NOT NULL,
    payload_preview TEXT NOT NULL,
    category TEXT NOT NULL,
    risk_score INTEGER NOT NULL,
    risk_level TEXT NOT NULL,
    reasons TEXT NOT NULL
)
"""


class EventStore:
    def __init__(self, database: Path):
        self.database = database
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            with connection:
                connection.execute(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=5)
        connection.row_factory = sqlite3.Row
        return connection

    def record(self, source_ip: str, source_port: int, service: str,
               payload: str, result: Classification) -> None:
        preview = "".join(char if char.isprintable() else "." for char in payload)[:200]
        with closing(self._connect()) as connection:
            with connection:
                connection.execute(
                    """INSERT INTO interactions
                    (timestamp_utc, source_ip, source_port, service, payload_preview,
                     category, risk_score, risk_level, reasons)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     source_ip, source_port, service, preview, result.category,
                     result.risk_score, risk_level(result.risk_score),
                     "; ".join(result.reasons)),
                )

    def recent(self, limit: int = 20) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT * FROM interactions ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def statistics(self) -> dict[str, Any]:
        with closing(self._connect()) as connection:
            total = connection.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
            unique_ips = connection.execute(
                "SELECT COUNT(DISTINCT source_ip) FROM interactions"
            ).fetchone()[0]
            high_risk = connection.execute(
                "SELECT COUNT(*) FROM interactions WHERE risk_level='high'"
            ).fetchone()[0]
            categories = connection.execute(
                "SELECT category, COUNT(*) AS count FROM interactions "
                "GROUP BY category ORDER BY count DESC, category"
            ).fetchall()
            top_ips = connection.execute(
                "SELECT source_ip, COUNT(*) AS count, MAX(risk_score) AS max_risk "
                "FROM interactions GROUP BY source_ip ORDER BY count DESC LIMIT 5"
            ).fetchall()
        return {
            "total_interactions": total,
            "unique_source_ips": unique_ips,
            "high_risk_interactions": high_risk,
            "categories": [dict(row) for row in categories],
            "top_sources": [dict(row) for row in top_ips],
        }
