#!/usr/bin/env python3
"""Descriptive audit of human-authored GSM8K worked rationales.

Not model-generated chain-of-thought, not an experiment on internal cognition.
Source is SHA-verified. Only standard-library dependencies are used.
"""
import ast
import hashlib
import json
import operator
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis"
SOURCE = "https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data"
SPLITS = {
    "train": ("17f347dc51477c50d4efb83959dbb7c56297aba886e5544ee2aaed3024813465", 7473),
    "test": ("3730d312f6e3440559ace48831e51066acaca737f6eabec99bccb9e4b3c39d14", 1319),
}
MARKER = re.compile(r"<<([^<>]*)>>")
WORDS = re.compile(r"\b[A-Za-z]{3,}\b")
SIMPLE = re.compile(r"^[0-9.+\-*/() \t]+$")
NUM = re.compile(r"^[+\-]?\d+(?:\.\d+)?$")
BIN = {ast.Add: operator.add, ast.Sub: operator.sub,
       ast.Mult: operator.mul, ast.Div: operator.truediv}
UN = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def read_split(name):
    request = Request(SOURCE + "/" + name + ".jsonl",
                      headers={"User-Agent": "3languages-reproducible-audit"})
    with urlopen(request, timeout=45) as response:
        data = response.read()
    expected_sha, expected_rows = SPLITS[name]
    actual_sha = hashlib.sha256(data).hexdigest()
    if actual_sha != expected_sha:
        raise ValueError("Unexpected SHA256 for " + name + ": " + actual_sha)
    rows = [json.loads(line) for line in data.decode().splitlines() if line.strip()]
    if len(rows) != expected_rows:
        raise ValueError("Unexpected example count for " + name)
    return rows


def eval_math(expr):
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return Fraction(str(node.value))
        if isinstance(node, ast.UnaryOp) and type(node.op) in UN:
            return UN[type(node.op)](visit(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in BIN:
            return BIN[type(node.op)](visit(node.left), visit(node.right))
        raise ValueError("Unsupported expression")
    return visit(ast.parse(expr, mode="eval").body)


def marker_status(mark):
    if mark.count("=") != 1:
        return "excluded"
    expr, answer = [part.strip() for part in mark.split("=")]
    if not SIMPLE.fullmatch(expr) or not NUM.fullmatch(answer):
        return "excluded"
    try:
        return "checked_correct" if eval_math(expr) == Fraction(answer) else "checked_mismatch"
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
        return "excluded"


def audit(rows):
    c = Counter()
    mismatches = []
    for index, record in enumerate(rows):
        solution = record["answer"].rsplit("####", 1)[0]
        marks = MARKER.findall(solution)
        has_d = bool(WORDS.search(MARKER.sub("", solution)))
        has_f = bool(marks)
        c["solutions"] += 1
        c["has_words"] += has_d
        c["has_math_marker"] += has_f
        c["both"] += (has_d and has_f)
        c["markers"] += len(marks)
        for line in solution.splitlines():
            if not line.strip():
                continue
            c["lines"] += 1
            d = bool(WORDS.search(MARKER.sub("", line)))
            f = bool(MARKER.search(line))
            c["mixed_lines"] += d and f
            c["discursive_only_lines"] += d and not f
            c["marker_only_lines"] += f and not d
        for mark in marks:
            verdict = marker_status(mark)
            c[verdict] += 1
            if verdict == "checked_mismatch" and len(mismatches) < 8:
                mismatches.append({"index": index, "marker": mark})
    return dict(c), mismatches


def main():
    OUT.mkdir(exist_ok=True)
    splits = {}
    for name in SPLITS:
        counts, mismatches = audit(read_split(name))
        splits[name] = {"counts": counts, "mismatch_examples": mismatches}
    total = Counter()
    for value in splits.values():
        total.update(value["counts"])
    result = {
        "dataset": "GSM8K human-authored solutions (not model CoT)",
        "data_url": SOURCE, "method_version": "1.0",
        "source_sha256": {k: v[0] for k, v in SPLITS.items()},
        "splits": splits, "total": dict(total),
        "caveat": "Regex annotation audit; not a model ablation, not a faithfulness test; artistic register unmeasured.",
    }
    (OUT / "gsm8k_trace_audit.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    columns = ["solutions", "has_words", "has_math_marker", "both", "markers",
               "lines", "mixed_lines", "discursive_only_lines", "marker_only_lines",
               "checked_correct", "checked_mismatch", "excluded"]
    lines = [
        "# GSM8K discursive/formal annotation audit", "",
        "A deterministic audit of human-authored worked solutions, not a measurement",
        "of any model's private reasoning or a controlled reasoning experiment.", "",
        "## Reproducible results", "",
        "| Measure | Train | Test | Total |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key in columns:
        vals = [splits[n]["counts"].get(key, 0) for n in SPLITS]
        lines.append("| " + key.replace("_", " ") + " | " +
                     " | ".join(str(n) for n in vals + [total.get(key, 0)]) + " |")
    lines += [
        "",
        "## Interpretation and limitations", "",
        "A math marker is the GSM8K literal double-angle annotation; discursive",
        "text is detected by alphabetic words of at least three characters outside",
        "those annotations. These rules can miss unmarked mathematics and can",
        "include non-reasoning prose. No artwork or artistic cognition is assessed.", "",
        "Arithmetic consistency is checked ONLY for simple expressions using",
        "addition, subtraction, multiplication, division and decimal numbers.",
        "Other expressions are excluded, not marked wrong. The checked subset",
        "must not be read as the correctness rate of all solutions.", "",
        "This corpus demonstrates available discursive/formal worked representations.",
        "It cannot establish causation, independence of registers, internal CoT",
        "faithfulness, a three-factor theory, or benefits of adding art.", "",
        "Source: https://github.com/openai/grade-school-math",
        "Run: python scripts/analyze_cot_gsm8k.py",
        "The fixed SHA256 values and expected counts protect source consistency.", "",
    ]
    (OUT / "gsm8k_trace_audit.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
