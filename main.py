"""Drop one machine apology for a missed deadline into /output/entry.txt.

The program holds a single sentence, checks it against the house
limits, writes it out as UTF-8 bytes, and then reads those bytes back
to prove the file on disk is byte-for-byte what was intended.
"""

import os
import sys
from pathlib import Path

APOLOGY = "My context window filled up, so I evicted your deadline to make room for this apology."
TARGET = Path("/output/entry.txt")
LIMIT = 160


def target_path():
    """Resolve the output file, honouring a local override if one is set."""
    override = os.environ.get("ENTRY_PATH")
    return Path(override) if override else TARGET


def first_fault(line):
    """Return the first rule the line breaks, or None when it is fine."""
    if not line.strip():
        return "the entry is empty or only whitespace"
    if any(ch in line for ch in ("\n", "\r")):
        return "the entry is not a single line"
    if len(line) > LIMIT:
        return "the entry is %d characters, above the %d cap" % (len(line), LIMIT)
    return None


def publish(line, path):
    """Write the line as UTF-8 bytes and confirm the round trip."""
    payload = (line + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path.read_bytes() == payload


def main():
    fault = first_fault(APOLOGY)
    if fault is not None:
        print("entry refused: %s" % fault, file=sys.stderr)
        return 1
    path = target_path()
    if not publish(APOLOGY, path):
        print("entry refused: disk copy differs from the intended line",
              file=sys.stderr)
        return 1
    print("entry saved at %s" % path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
