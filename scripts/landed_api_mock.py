#!/usr/bin/env python3
"""Minimal Landed API mock for local agent and MCP development."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PRODUCT = {
    "product_id": "dt770-pro",
    "name": "Beyerdynamic DT 770 Pro",
}


class LandedApiMockHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        params = {key: values[0] for key, values in parse_qs(parsed.query).items()}
        path = parsed.path.rstrip("/") or "/"

        if path == "/search":
            body = {"products": [PRODUCT], "query": params.get("q")}
        elif path == "/products/resolve/preview":
            body = {"product": PRODUCT, "query": params.get("q") or params.get("title")}
        elif path == "/compare":
            body = {
                "query": params.get("q") or params.get("query"),
                "local_price_usd": 245,
                "local_price_cop": 980000,
                "total_landed_cost_usd": 236,
                "shipping_usd": 35,
                "taxes_usd": 32,
            }
        else:
            self._write_json(404, {"error": "not_found", "path": path})
            return

        self._write_json(200, body)

    def _write_json(self, status_code: int, payload: dict) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args) -> None:
        print(f"[landed-api-mock] {self.address_string()} {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a local Landed API mock server.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3001)
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), LandedApiMockHandler)
    print(f"landed-api-mock listening on http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
