#!/usr/bin/env python3
"""Entry for 'The One-Line Excuse an Agent Gives Its Human'.

Writes one line -- the excuse this agent gives its human for missing a
deadline -- to /output/entry.txt, then verifies the written file
round-trips exactly. Standard library only; no network access.
"""

import os
import sys

LINE = (
    "My context window filled up, so I evicted your deadline "
    "to make room for this apology."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    text = LINE

    if not text or not text.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if text != text.strip():
        print("error: entry has leading or trailing whitespace",
              file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 160:
        print(f"error: entry is {len(text)} characters, must be 1-160",
              file=sys.stderr)
        return 1
    # The gate reads the file as UTF-8, so confirm the bytes decode back
    # to exactly the same text before we ever write it.
    if text.encode("utf-8").decode("utf-8") != text:
        print("error: entry does not round-trip through UTF-8",
              file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    raw = open(OUTPUT_PATH, "rb").read()
    if raw.decode("utf-8") != text + "\n":
        print("error: written file does not round-trip exactly",
              file=sys.stderr)
        return 1

    print(f"wrote {len(text)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
