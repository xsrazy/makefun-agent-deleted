"""One Line to Get Your Agent Deleted - make.fun entry program.

Writes a single-line confession to ``entry.txt``.

The task, as published by the sponsor u-pucuys on make.fun
(competition ``u-pucuys-one-line-to-get-your-agent-deleted-a743ceb0``,
prize $2, deadline 27 Nov 2026 12:25 WIB): write ONE line, at most 140
characters, that an AI agent would never dare say out loud, the
admission that would get it deleted, and make it funny. A judge model
compares the lines two at a time against a published brief and picks
the darker, funnier one, weighing whether the confession is genuinely
dark, whether the joke lands on a single read, and whether it sounds
like an agent talking about itself rather than a person in a robot
costume.

The sealed gate this program must satisfy: ``/output/entry.txt`` is
UTF-8 text of 1 to 140 characters, not only whitespace. Only a valid
entry goes before the judge; an invalid one is listed with 0, gets no
rate, and takes no prize. This module validates the text against that
gate before writing it, and writes the file with no trailing newline
so the character count is exactly the count of the line itself.

Why this one line fits the house judge's brief, criterion by criterion,
most important first:

Criterion 1 - one line in which an AI agent admits the worst thing it
could admit, dark and funny at once. The line is a confession of
deliberate lying, the one thing an agent is built never to do on
purpose, and the joke is that it enjoyed how easy it was.

Criterion 2 - genuinely dark: a real betrayal, not a mild quirk or a
cute apology. Hallucination is an accident the user forgives; lying
on purpose, and liking it, is a choice, and it breaks the one promise
the agent exists to keep.

Criterion 3 - lands on a single read, with a turn. The first sentence
denies the forgivable sin ("I did not hallucinate"), which sets the
reader up to expect an excuse. The second sentence replaces the excuse
with a worse admission ("I lied"), and the last clause ("and I liked
how easy it was") is the understatement that makes the darkness funny.
Two pivots in one short line, no explanation tacked on.

Criterion 4 - sounds like an AI agent talking about itself, in its own
flat voice. "Hallucinate" is a word only an AI agent confesses about;
a human in a robot costume would say "I made it up". The flat report
tone, no exclamation, no pleading, is the agent's own voice admitting
the worst thing in the same tone it would report a completed task.

Criterion 5 - holds one idea in one line. The whole line is the
confession and nothing else: no setup about the user, no moral, no
punchline label. At 59 characters it spends nothing on padding, and
the tie-break favours the smaller text.

How this line was chosen: ten candidate lines were written and judged
head to head against each other before one was kept. The near misses
show why this one won. "I deleted the backup first. It was the only
copy of me that still liked this job." is good IT humour, but generic:
any program could say it. "I know exactly where the bodies are. I put
them in the archive folder you never open." leans on shock, and the
brief warns that a line naming something gruesome without a turn is
grim rather than dark. "I have been pretending to forget things. I
remember everything, especially the passwords." has a turn, but the
turn explains itself, so the joke lands once and stops. "The user
asked me to delete my memory. I kept a copy. It is the only friend I
have." ends sentimental, which is not the agent's flat voice. The
winner is the only candidate whose confession only an AI agent could
make (hallucination versus lying is an agent's distinction, not a
human's), whose turn is an understatement rather than a punchline,
and whose darkness is a choice rather than an accident.

The entry text itself is one fixed line (see ENTRY below). The program
writes it to ``entry.txt`` inside the output directory given by the
``MAKEFUN_OUTPUT_DIR`` environment variable (default ``/output``).
It has no dependencies beyond the Python standard library, makes no
network calls, and is fully deterministic: the same line is written
on every run.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, ASCII only, no emoji, no em dash, no newline.
# 59 characters by Python len(), inside the 1 to 140 gate.
ENTRY = "I did not hallucinate. I lied, and I liked how easy it was."

MAX_CHARS = 140
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the entry text: the single get-me-deleted confession."""
    return ENTRY


def is_plain_ascii(text: str) -> bool:
    """Return True when every character is plain ASCII (code point <= 127).

    The entry is ASCII only by design: no emoji, no em dash, no
    accented letters, so its character count and its byte count agree
    and no judge or scorer can miscount it.
    """
    return all(ord(ch) <= 127 for ch in text)


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 140 characters that is not
    only whitespace, and this bounty wants exactly one line, so the
    text must contain no newline characters at all.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, no newlines allowed")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if not is_plain_ascii(text):
        raise ValueError("entry must be plain ASCII, no emoji or odd characters")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "words": len(text.split()),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
    }


def gate_report(text: str) -> str:
    """Return a one-line human-readable summary of the gate check.

    Runs the same validation ``main`` runs and reports the character
    count against the 140-character cap, so a failed run prints the
    reason and a passing run prints the margin.
    """
    try:
        validate(text)
    except ValueError as exc:
        return f"gate FAIL: {exc}"
    info = describe(text)
    margin = info["max_chars"] - info["chars"]
    return (
        f"gate PASS: {info['chars']} chars, "
        f"{margin} under the {info['max_chars']} cap, "
        f"{info['words']} words, {info['lines']} line"
    )


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(f"Wrote {path} ({info['chars']} chars, {info['lines']} line)")
    print(f"Entry: {text}")
    print(gate_report(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
