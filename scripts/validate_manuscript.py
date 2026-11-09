#!/usr/bin/env python3
"""Offline structural validator for the conceptual manuscript.

No external Python packages or web services are required.
This is a consistency check, NOT a substitute for full-text source review.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paper = (ROOT / "paper.md").read_text(encoding="utf-8")
bib = (ROOT / "references.bib").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
errors: list[str] = []

if "## References" not in paper:
    errors.append("paper.md lacks ## References")
    main, bibliography = paper, ""
else:
    main, bibliography = paper.split("## References", 1)

refs = [int(m.group(1)) for m in re.finditer(r"(?m)^(\d+)\.\s", bibliography)]
expected = list(range(1, len(refs) + 1))
if refs != expected:
    errors.append(f"Numbered references are not contiguous: {refs}")

# Capture both single citations [4] and groups such as [10,11] and [12-14].
cited: set[int] = set()
for match in re.finditer(r"\[([\d,\s-]+)\]", main):
    for token in match.group(1).split(","):
        token = token.strip()
        if not token:
            continue
        if re.fullmatch(r"\d+-\d+", token):
            lo, hi = (int(n) for n in token.split("-"))
            cited.update(range(lo, hi + 1))
        elif token.isdigit():
            cited.add(int(token))
missing = cited - set(refs)
unused = set(refs) - cited
if missing:
    errors.append(f"Citations without corresponding references: {sorted(missing)}")
if unused:
    errors.append(f"Bibliography entries never cited: {sorted(unused)}")

entries = [
    (int(m.group(1)), m.group(2))
    for m in re.finditer(
        r"(?ms)^@\w+\{\s*ref(\d\d)_[^,]+,(.*?)(?=^@\w+\{|\Z)", bib
    )
]
bib_numbers = [number for number, _ in entries]
if sorted(bib_numbers) != expected:
    errors.append(f"BibTeX identifiers do not match paper references: {bib_numbers}")

# DOI values are matched across the human-readable and machine-readable lists.
paper_dois = re.findall(r"https://doi\.org/([^\s]+)", bibliography)
bib_dois = [
    m.group(1) for _, entry in entries
    if (m := re.search(r"(?mi)^\s*doi\s*=\s*\{([^}]+)\}", entry))
]
if len(paper_dois) != len(bib_dois):
    errors.append(f"Different DOI counts: paper {len(paper_dois)}, BibTeX {len(bib_dois)}")
else:
    normalized = lambda values: sorted(v.strip().lower() for v in values)
    if normalized(paper_dois) != normalized(bib_dois):
        errors.append("Some paper and BibTeX DOI values disagree")

for required in (
    "## Abstract", "## 1. Introduction", "## 6. Testable propositions",
    "## 7. Quantitative and conceptual cautions", "## 10. Conclusion",
    "## Declarations", "## References"
):
    if required not in paper:
        errors.append(f"Missing required heading: {required}")

if len(main.split()) < 3000:
    errors.append("Conceptual article unusually short; review for missing content")
if len(refs) < 15:
    errors.append("Fewer than 15 literature references")
if "paper.md" not in readme:
    errors.append("README does not link to manuscript")

for name, content in (("paper.md", paper), ("README.md", readme), ("references.bib", bib)):
    if "\u2014" in content:
        errors.append(f"{name} contains an em dash")

if errors:
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    raise SystemExit(1)

print(f"PASS: {len(refs)} cited references, {len(entries)} BibTeX records, "
      f"{len(paper_dois)} DOI links, {len(main.split())} pre-bibliography words")
print("Note: structural validation only; it does not verify findings or source contents.")
