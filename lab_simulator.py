#!/usr/bin/env python3
"""Generate safe localhost-only interactions for demonstration."""

import argparse
import socket


PAYLOADS = [
    b"hello laboratory\n",
    b"USER admin PASS training-only\n",
    b"nmap service probe\n",
    b"curl http://example.invalid/training\n",
    b"' OR 1=1 --\n",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Send safe sample probes to local DecoyAI.")
    parser.add_argument("--port", type=int, default=2222)
    args = parser.parse_args()
    for payload in PAYLOADS:
        with socket.create_connection(("127.0.0.1", args.port), timeout=2) as connection:
            connection.recv(1024)
            connection.sendall(payload)
            connection.recv(1024)
        print(f"[LAB] Sent sample: {payload.decode().strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
