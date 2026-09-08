"""Local security statistics dashboard."""

from __future__ import annotations

import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .storage import EventStore


STYLE = """
body{font-family:system-ui;background:#07111f;color:#dbeafe;margin:0}main{max-width:1100px;margin:auto;padding:30px}
h1{color:#67e8f9}.notice{background:#13233a;border-left:4px solid #22d3ee;padding:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:24px 0}
.card{background:#101d31;border:1px solid #274060;border-radius:12px;padding:18px}.value{font-size:32px;font-weight:700;color:#a7f3d0}table{width:100%;border-collapse:collapse;background:#101d31}th,td{padding:10px;border-bottom:1px solid #274060;text-align:left}.high{color:#fca5a5}.medium{color:#fde68a}.low{color:#a7f3d0}code{color:#bae6fd}
"""


def page(store: EventStore) -> str:
    stats, recent = store.statistics(), store.recent()
    cards = [("Interactions", stats["total_interactions"]),
             ("Unique sources", stats["unique_source_ips"]),
             ("High risk", stats["high_risk_interactions"]),
             ("Categories", len(stats["categories"]))]
    card_html = "".join(f'<div class="card"><div>{html.escape(k)}</div><div class="value">{v}</div></div>' for k,v in cards)
    rows = "".join(
        f"<tr><td>{html.escape(row['timestamp_utc'])}</td><td>{html.escape(row['source_ip'])}</td>"
        f"<td>{html.escape(row['category'])}</td><td class=\"{row['risk_level']}\">{html.escape(row['risk_level'])}</td>"
        f"<td>{row['risk_score']}</td><td><code>{html.escape(row['payload_preview'])}</code></td></tr>"
        for row in recent
    ) or '<tr><td colspan="6">No laboratory interactions recorded yet.</td></tr>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="5"><title>DecoyAI Dashboard</title><style>{STYLE}</style></head>
<body><main><h1>DecoyAI Security Dashboard</h1><p class="notice">Local laboratory dashboard. Data refreshes every five seconds.</p>
<div class="grid">{card_html}</div><h2>Recent interactions</h2><table><thead><tr><th>UTC time</th><th>Source</th><th>Category</th><th>Risk</th><th>Score</th><th>Payload preview</th></tr></thead><tbody>{rows}</tbody></table></main></body></html>"""


def handler_for(store: EventStore):
    class DashboardHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/api/stats":
                body = json.dumps(store.statistics()).encode()
                content_type = "application/json"
            elif self.path == "/":
                body = page(store).encode()
                content_type = "text/html; charset=utf-8"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; refresh-src 'self'")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args) -> None:
            return
    return DashboardHandler


def create_dashboard(address: tuple[str, int], store: EventStore) -> ThreadingHTTPServer:
    if address[0] not in {"127.0.0.1", "localhost"}:
        raise ValueError("Dashboard is restricted to localhost for safety.")
    return ThreadingHTTPServer(address, handler_for(store))
