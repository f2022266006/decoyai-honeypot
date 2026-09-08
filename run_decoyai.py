#!/usr/bin/env python3
"""Start DecoyAI's local fake service and web dashboard."""

from __future__ import annotations

import argparse
import signal
import threading
from pathlib import Path

from decoyai.dashboard import create_dashboard
from decoyai.service import ThreadedDecoyServer
from decoyai.storage import EventStore


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the localhost-only DecoyAI laboratory honeypot.")
    parser.add_argument("--decoy-port", type=int, default=2222)
    parser.add_argument("--dashboard-port", type=int, default=8080)
    parser.add_argument("--database", type=Path, default=Path("data/decoyai.db"))
    args = parser.parse_args()

    store = EventStore(args.database)
    decoy = ThreadedDecoyServer(("127.0.0.1", args.decoy_port), store)
    dashboard = create_dashboard(("127.0.0.1", args.dashboard_port), store)
    threads = [threading.Thread(target=server.serve_forever, daemon=True) for server in (decoy, dashboard)]
    for thread in threads:
        thread.start()
    print(f"[SAFE MODE] Fake service: 127.0.0.1:{args.decoy_port}")
    print(f"[DASHBOARD] http://127.0.0.1:{args.dashboard_port}")
    print("Press Ctrl+C to stop.")

    stopped = threading.Event()
    def stop(_signum=None, _frame=None):
        stopped.set()
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    stopped.wait()
    decoy.shutdown(); dashboard.shutdown()
    decoy.server_close(); dashboard.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
