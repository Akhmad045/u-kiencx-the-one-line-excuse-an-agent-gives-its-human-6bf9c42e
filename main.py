"""Save a single-sentence machine apology for a missed deadline.

Running this file drops one short line of text at /output/entry.txt and
then reads the file back to make sure what landed on disk is exactly
what was meant to be written. Nothing else is produced.
"""

import os
import sys

APOLOGY = "My context window filled up, so I evicted your deadline to make room for this apology."
DESTINATION = "/output/entry.txt"
CEILING = 160


def destination():
    """Where the line goes; an env override exists for local try-outs."""
    return os.environ.get("ENTRY_PATH", DESTINATION)


def problems(line):
    """Collect every way the line would break the house rules."""
    found = []
    if not line.strip():
        found.append("the line is blank")
    if "\n" in line or "\r" in line:
        found.append("the line spills across more than one line")
    if len(line) > CEILING:
        found.append(
            "the line runs %d characters, past the %d limit" % (len(line), CEILING)
        )
    return found


def store(line, path):
    """Write the line plus a trailing newline as UTF-8 text."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")


def confirm(line, path):
    """Read the file back and check it matches the line exactly."""
    with open(path, "r", encoding="utf-8") as handle:
        back = handle.read()
    return back == line + "\n"


def main():
    faults = problems(APOLOGY)
    if faults:
        for fault in faults:
            print("cannot write entry: %s" % fault, file=sys.stderr)
        return 1
    path = destination()
    store(APOLOGY, path)
    if not confirm(APOLOGY, path):
        print(
            "cannot write entry: the file read back differently",
            file=sys.stderr,
        )
        return 1
    print("entry written to %s" % path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
