"""Validate the MCP Server Registry README.

Guards three classes of drift that have actually happened in this repo:

1. The Registry Stats table counts servers/categories that do not match the
   catalog. It claimed 36 servers and 14 categories while the catalog held
   26 entries in 9 categories, and an external PR added an entry without
   touching the table.
2. The stats heading date and the footer 'Last updated' date disagree.
3. A server entry is added with no description, or a duplicate name is
   added, or a code fence is left unbalanced.

Run directly:  python3 scripts/validate_registry.py
Exit code 0 = valid, 1 = problems found.
"""

import pathlib
import re
import sys

README = pathlib.Path(__file__).resolve().parents[1] / "README.md"

# The catalog lives between these two headings. Everything inside is a
# server entry (H4) or a category (H3).
CATALOG_START = "## Official & Community Servers"
CATALOG_END = "## MCP Server by Use Case"

ENTRY_RE = re.compile(r"^#### `([^`]+)`(.*)$")
CATEGORY_RE = re.compile(r"^### (?!.*\()")
STATS_RE = re.compile(r"^\| (Servers in this registry|Categories covered) \| ([0-9]+) \|$")


def _strip_fences(lines):
    """Yield (index, line) for lines outside fenced code blocks."""
    in_fence = False
    fence = None
    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            if not in_fence:
                in_fence = True
                fence = idx
            else:
                in_fence = False
                fence = None
            continue
        if not in_fence:
            yield idx, line


def main():
    if not README.is_file():
        print(f"FAIL: {README} is missing")
        return 1

    raw = README.read_text(encoding="utf-8")
    lines = raw.split("\n")
    problems = []

    # --- code fences must be balanced ---
    fence_count = sum(1 for ln in lines if ln.lstrip().startswith("```"))
    if fence_count % 2 != 0:
        problems.append(f"unbalanced code fences: {fence_count} ``` markers")

    # --- catalog section ---
    try:
        start = lines.index(CATALOG_START)
        end = lines.index(CATALOG_END)
    except ValueError as exc:
        print(f"FAIL: catalog headings not found ({exc})")
        return 1

    catalog = lines[start:end]

    entries = []
    categories = []
    for idx, line in enumerate(catalog):
        if line.startswith("#### "):
            m = ENTRY_RE.match(line)
            if m:
                entries.append((idx, m.group(1), m.group(2).strip()))
        elif line.startswith("### "):
            categories.append((idx, line[4:].strip()))

    if not entries:
        problems.append("catalog contains no server entries")

    # --- duplicate names ---
    seen = {}
    for idx, name, _qual in entries:
        if name in seen:
            problems.append(f"duplicate server entry: {name!r}")
        seen[name] = idx

    # --- every entry needs a description line ---
    for pos, (idx, name, _qual) in enumerate(entries):
        end_idx = entries[pos + 1][0] if pos + 1 < len(entries) else len(catalog)
        body = [ln for ln in catalog[idx + 1:end_idx] if ln.strip()]
        if not body:
            problems.append(f"entry {name!r} has no description")

    # --- stats table must match the catalog ---
    stats = {}
    for idx, line in enumerate(lines):
        m = STATS_RE.match(line.strip())
        if m:
            stats[m.group(1)] = (int(m.group(2)), idx + 1)

    if "Servers in this registry" not in stats:
        problems.append("Registry Stats table has no 'Servers in this registry' row")
    elif stats["Servers in this registry"][0] != len(entries):
        claimed, lineno = stats["Servers in this registry"]
        problems.append(
            f"Registry Stats claims {claimed} servers but the catalog has "
            f"{len(entries)} (README line {lineno})"
        )

    if "Categories covered" not in stats:
        problems.append("Registry Stats table has no 'Categories covered' row")
    elif stats["Categories covered"][0] != len(categories):
        claimed, lineno = stats["Categories covered"]
        problems.append(
            f"Registry Stats claims {claimed} categories but the catalog has "
            f"{len(categories)} (README line {lineno})"
        )

    # --- stats heading month must match the footer 'Last updated' month ---
    heading_date = None
    for line in lines:
        m = re.match(r"^## Registry Stats \((.+?)\)$", line.strip())
        if m:
            heading_date = m.group(1).strip()
            break
    footer_date = None
    m = re.search(r"Last updated: ([A-Za-z]+ [0-9]{4})", raw)
    if m:
        footer_date = m.group(1).strip()
    if heading_date is None:
        problems.append("no '## Registry Stats (Month YYYY)' heading found")
    if footer_date is None:
        problems.append("no 'Last updated: Month YYYY' footer found")
    if heading_date and footer_date and heading_date != footer_date:
        problems.append(
            f"Registry Stats heading says {heading_date!r} but the footer says "
            f"{footer_date!r}"
        )

    if problems:
        print("FAIL: registry README validation failed")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(
        f"OK: {len(entries)} servers across {len(categories)} categories; "
        f"stats table and dates agree (as of {footer_date})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
