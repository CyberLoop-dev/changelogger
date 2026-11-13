#!/usr/bin/env python3
"""changelogger: turn Conventional Commits into a Markdown changelog.

Usage:
    python changelogger.py                  # latest tag -> HEAD
    python changelogger.py --from v1.0.0 --to v1.1.0 --version 1.1.0
    python changelogger.py -o CHANGELOG.md
"""
import argparse
import datetime
import re
import subprocess
import sys

SECTIONS = [
    ("breaking", "💥 Breaking changes"),
    ("feat", "✨ Features"),
    ("fix", "🐛 Bug fixes"),
    ("perf", "⚡ Performance"),
    ("refactor", "♻️ Refactoring"),
    ("docs", "📚 Documentation"),
    ("test", "✅ Tests"),
    ("build", "📦 Build"),
    ("ci", "🤖 CI"),
    ("chore", "🧹 Chores"),
    ("style", "🎨 Style"),
    ("revert", "⏪ Reverts"),
    ("other", "🔹 Other"),
]
PATTERN = re.compile(r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?: (?P<subject>.+)$")


def git(*args):
    try:
        res = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")
    except FileNotFoundError:
        sys.exit("changelogger: git is not installed")
    if res.returncode != 0:
        sys.exit("changelogger: " + (res.stderr.strip() or "git failed"))
    return res.stdout


def latest_tag():
    res = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True)
    return res.stdout.strip() if res.returncode == 0 else None


def commits(rev_range):
    fmt = "%h%x1f%s%x1f%b%x1e"
    raw = git("log", "--no-merges", f"--pretty=format:{fmt}", *([rev_range] if rev_range else []))
    for rec in raw.split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        sha, subject, body = (rec.split("\x1f") + ["", ""])[:3]
        yield sha.strip(), subject.strip(), body


def group(items):
    buckets = {k: [] for k, _ in SECTIONS}
    for sha, subject, body in items:
        m = PATTERN.match(subject)
        if m:
            kind = m["type"].lower()
            kind = kind if kind in buckets else "other"
            entry = (m["scope"], m["subject"], sha)
            if m["bang"] or "BREAKING CHANGE" in body:
                buckets["breaking"].append(entry)
                if m["bang"]:
                    continue
            if not (m["bang"]):
                buckets[kind].append(entry)
        else:
            buckets["other"].append((None, subject, sha))
    return buckets


def render(buckets, title, link_base):
    lines = [f"## {title}", ""]
    empty = True
    for key, heading in SECTIONS:
        if not buckets[key]:
            continue
        empty = False
        lines += [f"### {heading}", ""]
        for scope, subject, sha in buckets[key]:
            ref = f"[`{sha}`]({link_base}/commit/{sha})" if link_base else f"`{sha}`"
            lines.append(f"- {f'**{scope}:** ' if scope else ''}{subject} ({ref})")
        lines.append("")
    if empty:
        lines += ["_No changes._", ""]
    return "\n".join(lines)


def repo_link():
    res = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    url = res.stdout.strip()
    m = re.match(r"(?:git@([^:]+):|https?://([^/]+)/)(.+?)(?:\.git)?$", url)
    if not m:
        return None
    return f"https://{m.group(1) or m.group(2)}/{m.group(3)}"


def main():
    ap = argparse.ArgumentParser(description="Generate a changelog from Conventional Commits.")
    ap.add_argument("--from", dest="start", help="start ref (default: latest tag, or the whole history)")
    ap.add_argument("--to", dest="end", default="HEAD", help="end ref (default: HEAD)")
    ap.add_argument("--version", help="heading for this release (default: end ref or 'Unreleased')")
    ap.add_argument("--no-links", action="store_true", help="do not link commit hashes")
    ap.add_argument("-o", "--output", help="write to a file instead of stdout")
    a = ap.parse_args()

    start = a.start or latest_tag()
    rng = f"{start}..{a.end}" if start else a.end
    title = a.version or ("Unreleased" if a.end == "HEAD" else a.end)
    title += f" ({datetime.date.today().isoformat()})"

    buckets = group(commits(rng))
    text = render(buckets, title, None if a.no_links else repo_link())
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"wrote {a.output}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
