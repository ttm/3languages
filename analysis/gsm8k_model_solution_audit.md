# GSM8K archived model-generated solutions: descriptive audit

This analysis inspects the published sample of generated model solutions,
not internal private chain-of-thought. Correctness labels are supplied
by the dataset authors and are not independently re-evaluated.

The original GSM8K paper notes that these archived model samples
used an older calculator implementation with occasional bugs.

Source: https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/example_model_solutions.jsonl

Git blob SHA1: 95472c66429c88ca96d09031d9624fece293081a

Questions represented: 1319

## Model/configuration summaries

| Arm | Solutions | Labeled correct | With prose and annotated arithmetic | Correct among both | Incorrect despite all parsed markers arithmetically consistent |
| --- | ---: | ---: | ---: | ---: | ---: |
| 6b finetuning | 1319 | 286 | 1312 | 286 | 1016 |
| 6b verification | 1319 | 515 | 1314 | 514 | 785 |
| 175b finetuning | 1319 | 458 | 1301 | 454 | 828 |
| 175b verification | 1319 | 742 | 1301 | 740 | 555 |

## Calculation annotation audit

| Arm | Marker spans | Exact arithmetic agrees | Exact arithmetic disagrees | Excluded from restricted parser |
| --- | ---: | ---: | ---: | ---: |
| 6b finetuning | 4196 | 4064 | 121 | 11 |
| 6b verification | 4047 | 3998 | 26 | 23 |
| 175b finetuning | 4210 | 4076 | 110 | 24 |
| 175b verification | 4240 | 4208 | 26 | 6 |

## Interpretation constraints

- This is a **selected published sample**, not the full distribution of all model outputs.
- Model size, fine-tuning/verification, and calculator behavior differ between arms; differences are not treatment effects.
- Arithmetic agreement in a marked span does not establish sound reasoning or a correct answer.
- A missing marker does not mean the solution contains no mathematical reasoning.
- The data are textual and mathematical; **no artistic register is measured**.
- Presence of visible rationale content does not demonstrate internal CoT faithfulness.
- Reproduction: python scripts/analyze_cot_model_samples.py.
