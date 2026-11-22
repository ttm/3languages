# GSM8K discursive/formal annotation audit

A deterministic audit of human-authored worked solutions, not a measurement
of any model's private reasoning or a controlled reasoning experiment.

## Reproducible results

| Measure | Train | Test | Total |
| --- | ---: | ---: | ---: |
| solutions | 7473 | 1319 | 8792 |
| has words | 7472 | 1319 | 8791 |
| has math marker | 7378 | 1301 | 8679 |
| both | 7377 | 1301 | 8678 |
| markers | 23716 | 4282 | 27998 |
| lines | 26720 | 4819 | 31539 |
| mixed lines | 23578 | 4257 | 27835 |
| discursive only lines | 2735 | 489 | 3224 |
| marker only lines | 138 | 25 | 163 |
| checked correct | 23634 | 4266 | 27900 |
| checked mismatch | 0 | 0 | 0 |
| excluded | 82 | 16 | 98 |

## Interpretation and limitations

A math marker is the GSM8K literal double-angle annotation; discursive
text is detected by alphabetic words of at least three characters outside
those annotations. These rules can miss unmarked mathematics and can
include non-reasoning prose. No artwork or artistic cognition is assessed.

Arithmetic consistency is checked ONLY for simple expressions using
addition, subtraction, multiplication, division and decimal numbers.
Other expressions are excluded, not marked wrong. The checked subset
must not be read as the correctness rate of all solutions.

This corpus demonstrates available discursive/formal worked representations.
It cannot establish causation, independence of registers, internal CoT
faithfulness, a three-factor theory, or benefits of adding art.

Source: https://github.com/openai/grade-school-math
Run: python scripts/analyze_cot_gsm8k.py
The fixed SHA256 values and expected counts protect source consistency.
