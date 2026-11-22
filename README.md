# Three Languages Hypothesis

An academic working paper about the hypothesis that **natural language, mathematical formalism, and the arts** are three major forms of knowledge production and transmission.

**[Read manuscript](paper.md)** | **[Read PDF](paper.pdf)**

**Title:** *The Three Languages Hypothesis: Natural Language, Mathematics, and Art as Epistemic Registers*  
**Last updated:** 22 November 2026  
**Status:** Working conceptual and hypothesis paper, not peer reviewed or submitted.  
**Sources:** 34 references, available in [paper.md](paper.md) and [references.bib](references.bib).

## Argument

The paper takes the 2026 three-languages proposition by [Oliveira Jr. and Oliveira](https://www.comciencia.br/porque-maquinas-inteligentes-poderao-superar-os-seres-humanos/) as its object of critical inquiry. Its central reconstruction distinguishes **discursive**, **formal-relational**, and **aesthetic-experiential** registers. These are neither mutually exclusive media nor three cognitive modules.

It distinguishes **prominence**, **complementarity**, **completeness**, and **universal sufficiency**. Only the first two are advanced as bounded hypotheses. Strong sufficiency is not established.

## Chain-of-thought study and original data audit

- The revised manuscript examines verbal CoT, executable reasoning, visual sketching, latent reasoning, and CoT faithfulness, as well as Fodor's Language of Thought and 2026 multimodal-CoT counterevidence.
- Completed SHA-verified descriptive GSM8K audit: 8,792 human-authored solutions, 8,678 with both prose and explicitly marked arithmetic, and 27,900 simple arithmetic annotations independently checked.
- [Reproducible audit report](analysis/gsm8k_trace_audit.md), [JSON data](analysis/gsm8k_trace_audit.json), and [Python script](scripts/analyze_cot_gsm8k.py).
- Model-generated audit: [5,276 emitted solutions across four model variants](analysis/gsm8k_model_solution_audit.md), [machine-readable counts](analysis/gsm8k_model_solution_audit.json), and [reproduction script](scripts/analyze_cot_model_samples.py). Local arithmetic checks must not be confused with correct inference or internal CoT faithfulness.
- Future research: process-labeled PRM800K, multimodal ScienceQA, and aesthetic interpretation in ArtEmis, with matched interventions to test D/F/A complementarity.
- No model performance ablation, independent ArtEmis analysis, or cognitive three-factor finding is claimed.

## What's new

- The three-languages hypothesis is central; sensory stimulation is only a short side note.
- Key antecedents: Cassirer, Goodman, Peirce, Bruner, Paivio, diagrammatic reasoning, and cognitive theories of grounding.
- Serious counterarguments: heterogeneous categories, tacit skills, artistic knowledge debates, alternative taxonomies, and the gap between expression and action.
- An explicit model of representation-dependent transformation and preservation.
- Five testable propositions, including comparison against rival two-, three-, four-, and continuous-dimensional taxonomies.
- Philosophical and technological consequences, including verifiable AI translation between representational registers.

## Editorial requirements before publication

- [ ] Independent scholarly review in philosophy of science, aesthetics, semiotics, and cognitive science.
- [ ] Verify every source against its publisher record and full text, including 2026 works.
- [ ] Confirm authorship, affiliations, contributions, disclosures, and financing.
- [ ] Predefine coding rubrics and register-sensitive outcome measures for any proposed tests.
- [ ] Select a venue and manuscript license.

The manuscript does not report new experimental evidence, demonstrate a latent three-factor structure, or claim all human skills reduce to three modes of expression.

## Build

`paper.md` is the canonical source. GitHub Actions builds and commits `paper.pdf` using `scripts/build_pdf.sh` when the manuscript changes. `python scripts/validate_manuscript.py` checks structural citation consistency only, not scientific validity.

No explicit license has been selected.
