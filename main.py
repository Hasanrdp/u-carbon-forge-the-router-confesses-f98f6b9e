#!/usr/bin/env python3
"""The Router Confesses — u-carbon-forge-the-router-confesses-f98f6b9e.

Writes one line to /output/entry.txt: the excuse a home Wi-Fi router gives
for dropping the connection at the exact moment a movie reaches its climax.

The line is pinned below with its exact byte count and SHA-256. The program
writes it, reads it back, and refuses to report success unless the bytes on
disk match the pin exactly. Pure standard library, deterministic, no network,
no randomness, no input read.
"""

import hashlib
import os
import sys

LINE = "I didn't drop you \u2014 I saw the killer's face first, and I needed a minute alone with that information."

EXPECTED_CHARS = 101
EXPECTED_BYTES = 103
EXPECTED_SHA256 = "1c71dbf37477661a9c711269d974b672920253be041c6043e4c8e7a38b8cb426"


def output_path() -> str:
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(base, "entry.txt")


def verify(path: str) -> None:
    with open(path, "rb") as fh:
        data = fh.read()
    text = data.decode("utf-8")
    if len(text) != EXPECTED_CHARS:
        raise SystemExit(f"verify: {len(text)} chars, expected {EXPECTED_CHARS}")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(f"verify: {len(data)} bytes, expected {EXPECTED_BYTES}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"verify: sha256 {digest}, expected {EXPECTED_SHA256}")
    if text != LINE:
        raise SystemExit("verify: text does not match the pinned line")


def main() -> int:
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(LINE)
    verify(path)
    print(f"wrote {path}: {EXPECTED_BYTES} bytes, sha256 {EXPECTED_SHA256}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
