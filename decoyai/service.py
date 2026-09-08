"""Localhost-only fake TCP service."""

from __future__ import annotations

import socketserver

from .classifier import classify
from .storage import EventStore


BANNER = b"SSH-2.0-DecoyAI_Lab_1.0\r\n"


class DecoyHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        self.request.settimeout(2)
        self.request.sendall(BANNER)
        try:
            raw = self.request.recv(1024)
        except (TimeoutError, OSError):
            raw = b""
        payload = raw.decode("utf-8", errors="replace")
        result = classify(payload)
        self.server.store.record(
            self.client_address[0], self.client_address[1],
            "fake-ssh", payload, result
        )
        try:
            self.request.sendall(b"Access denied. Laboratory decoy.\r\n")
        except OSError:
            pass


class ThreadedDecoyServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address: tuple[str, int], store: EventStore):
        if address[0] not in {"127.0.0.1", "localhost"}:
            raise ValueError("DecoyAI is restricted to localhost for safety.")
        self.store = store
        super().__init__(address, DecoyHandler)
