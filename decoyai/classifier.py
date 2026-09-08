"""Explainable suspicious-behaviour classification rules."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Classification:
    category: str
    risk_score: int
    reasons: tuple[str, ...]


RULES = (
    ("command_probe", 80, re.compile(r"\b(?:wget|curl|chmod|powershell|/bin/sh|cmd\.exe)\b", re.I), "command or download keyword"),
    ("injection_probe", 75, re.compile(r"(?:'\s*or\s+1=1|union\s+select|\.\./|<script)", re.I), "injection or traversal pattern"),
    ("credential_probe", 55, re.compile(r"\b(?:login|user(?:name)?|pass(?:word)?|admin|root)\b", re.I), "credential-related keyword"),
    ("scanner_probe", 45, re.compile(r"\b(?:nmap|masscan|zgrab|nikto|sqlmap)\b", re.I), "scanner signature"),
)


def classify(payload: str) -> Classification:
    """Classify text without executing or interpreting it as a command."""
    matches: list[tuple[str, int, str]] = []
    for category, score, pattern, reason in RULES:
        if pattern.search(payload):
            matches.append((category, score, reason))
    if not payload.strip():
        return Classification("empty_probe", 20, ("connected without sending data",))
    if not matches:
        return Classification("unknown_probe", 10, ("no known signature matched",))
    category, score, _ = max(matches, key=lambda item: item[1])
    return Classification(category, score, tuple(item[2] for item in matches))


def risk_level(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"
