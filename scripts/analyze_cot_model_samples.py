#!/usr/bin/env python3
"""Describe archived GSM8K model-generated worked solutions.

The dataset contains four historical model configurations and author-supplied
is_correct labels. These are emitted text traces, not internal hidden states.
Analyses are descriptive and non-causal.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen
from analyze_cot_gsm8k import MARKER, WORDS, marker_status

ROOT = Path(__file__).resolve().parents[1]
URL = "https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/example_model_solutions.jsonl"
GIT_BLOB_SHA1 = "95472c66429c88ca96d09031d9624fece293081a"
EXPECTED_BYTES = 2563513
ARMS = ("6b_finetuning", "6b_verification", "175b_finetuning", "175b_verification")


def fetch():
    req = Request(URL, headers={"User-Agent": "3languages-reproducible-model-audit"})
    with urlopen(req, timeout=45) as response:
        blob = response.read()
    git_sha = hashlib.sha1(b"blob " + str(len(blob)).encode() + b"\0" + blob).hexdigest()
    if git_sha != GIT_BLOB_SHA1 or len(blob) != EXPECTED_BYTES:
        raise ValueError("Data do not match GitHub's pinned blob identity")
    return [json.loads(x) for x in blob.decode("utf-8").splitlines() if x.strip()]


def main():
    rows = fetch()
    output = {
        "dataset": "Archived GSM8K example_model_solutions.jsonl",
        "source": URL, "git_blob_sha1": GIT_BLOB_SHA1,
        "sha256": None,
        "examples": len(rows),
        "model_configurations": {},
        "caution": "Historical, selected outputs; author-provided correctness labels; no causal inference or model-internal CoT access.",
    }
    for arm in ARMS:
        c = Counter()
        for i, item in enumerate(rows):
            x = item[arm]
            answer = x["solution"]
            correct = x["is_correct"]
            if not isinstance(answer, str) or not isinstance(correct, bool):
                raise TypeError("Unexpected answer field schema")
            marks = MARKER.findall(answer)
            d = bool(WORDS.search(MARKER.sub("", answer)))
            f = bool(marks)
            results = Counter(marker_status(m) for m in marks)
            c["samples"] += 1
            c["labeled_correct"] += correct
            c["with_discursive_words"] += d
            c["with_calculation_markers"] += f
            c["both_discursive_and_marked"] += (d and f)
            c["both_and_correct"] += (d and f and correct)
            c["without_both"] += (not (d and f))
            c["without_both_and_correct"] += (not (d and f) and correct)
            c["markers"] += len(marks)
            c["checked_arith_correct"] += results["checked_correct"]
            c["checked_arith_mismatch"] += results["checked_mismatch"]
            c["excluded_arith"] += results["excluded"]
            if f and results["checked_arith_mismatch"] == 0 and results["excluded"] == 0 and not correct:
                c["incorrect_with_all_markers_arith_checked_correct"] += 1
        output["model_configurations"][arm] = dict(c)
    target = ROOT / "analysis"
    target.mkdir(exist_ok=True)
    (target / "gsm8k_model_solution_audit.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# GSM8K archived model-generated solutions: descriptive audit", "",
        "This analysis inspects the published sample of generated model solutions,",
        "not internal private chain-of-thought. Correctness labels are supplied",
        "by the dataset authors and are not independently re-evaluated.", "",
        "The original GSM8K paper notes that these archived model samples",
        "used an older calculator implementation with occasional bugs.", "",
        "Source: " + URL, "",
        "Git blob SHA1: " + GIT_BLOB_SHA1, "",
        "Questions represented: " + str(len(rows)), "",
        "## Model/configuration summaries", "",
        "| Arm | Solutions | Labeled correct | With prose and annotated arithmetic | Correct among both | Incorrect despite all parsed markers arithmetically consistent |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for arm in ARMS:
        c = output["model_configurations"][arm]
        lines.append("| " + arm.replace("_", " ") + " | " +
                     " | ".join(str(c.get(k, 0)) for k in (
                         "samples", "labeled_correct", "both_discursive_and_marked",
                         "both_and_correct", "incorrect_with_all_markers_arith_checked_correct")) + " |")
    lines += ["", "## Calculation annotation audit", "",
              "| Arm | Marker spans | Exact arithmetic agrees | Exact arithmetic disagrees | Excluded from restricted parser |",
              "| --- | ---: | ---: | ---: | ---: |"]
    for arm in ARMS:
        c = output["model_configurations"][arm]
        lines.append("| " + arm.replace("_", " ") + " | " +
                     " | ".join(str(c.get(k, 0)) for k in (
                         "markers", "checked_arith_correct",
                         "checked_arith_mismatch", "excluded_arith")) + " |")
    lines += ["", "## Interpretation constraints", "",
              "- This is a **selected published sample**, not the full distribution of all model outputs.",
              "- Model size, fine-tuning/verification, and calculator behavior differ between arms; differences are not treatment effects.",
              "- Arithmetic agreement in a marked span does not establish sound reasoning or a correct answer.",
              "- A missing marker does not mean the solution contains no mathematical reasoning.",
              "- The data are textual and mathematical; **no artistic register is measured**.",
              "- Presence of visible rationale content does not demonstrate internal CoT faithfulness.",
              "- Reproduction: python scripts/analyze_cot_model_samples.py.", ""]
    (target / "gsm8k_model_solution_audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
