# Evidence map and research notes

Source: Jaehyun Nam, Jinsung Yoon, Yanzhou Pan, Yubo Wang, Rui Meng, Parthasarathy Ranganathan and Tomas Pfister, **ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI**, [arXiv:2609.19644v1](https://arxiv.org/abs/2609.19644v1). Original material: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This file is an attributed analytical adaptation. It is not an author-provided prompt or official implementation.

Page references below are **physical PDF pages**, including figures and appendix. PDF bookmarks sometimes point one page before the printed heading; use the per-page cache to confirm.

## Rule-to-source mapping

| Skill principle | Source in paper | Preserved mechanism | Adaptation made here |
|---|---|---|---|
| Limitations before ideas | §3.1, p6 | Limitation extractor/verifier loop; novelty-ranked seed pool | A single agent can perform separate passes; literature search scope stays explicit |
| Baseline before modification | §3.2, pp6–7 | Reproduce a subset baseline; modify its code for candidates | Record reproduction gaps and aligned conditions explicitly |
| Good / Engineer / Bad | §3.2, pp6–7 | Critic decision, bounded engineering, prune exhausted candidates | No invented universal numerical improvement threshold |
| Subset before full suite | §3.2, pp6–7 | Promote good candidates to full-set evaluation and critique | Subset results cannot support a full-suite claim |
| Refine from all traces | §3.3, pp7–8 | Historic success/failure traces; evolved ideas plus unused seeds | Persistent experiment records, without requiring a multi-agent service |
| Best state survives failed revisions | §§3.4, 3.6, pp8–10 | Replace best only after comparison; retain previous outputs on failed meta-refinement | Keep the code/result/claim revision linked |
| Ablation as method development | §3.4, p8 | Component tests feed back into method; repeat after changes | Aligned compute/data controls made explicit |
| Experimental rebuttal | §3.5, pp8–9 | Reviewer → supplementary experiment plan → execution → manuscript enhancement | Requested review can be a separate pass; not necessarily a separate agent |
| Meta-review can reopen research | §3.6, pp9–10 | Criticism can change method, rerun ablations and redraft | No automatic submission or asserted conference acceptance |
| Four integrity checks | §4.2, pp14–15, Table7 | Score verification, task specification, citations, method–code alignment | Report which checks actually ran; no inferred audit pass |
| Finite search | Listing1 p5; §3; Appendix A configuration p30 | Bounded critic/refinement loops | User's budget and scope replace published default counts |

## What the system actually does

Inputs are a scientific problem and relevant prior research/code. Output is an improved manuscript paired with an executable codebase. Table1 (p5) specifies candidate, critic and refinement roles for each stage; Figure3 presents the orchestration. This is a system for empirical research, not simply literature summarization or text generation.

The method comprises seed generation, subset/full-set evaluation, result-driven idea evolution, component ablations, drafting with simulated review/rebuttal, and meta-review. Feedback has several depths: code engineering for a promising idea, a new hypothesis from experimental traces, removing/revising components from ablations, new experiments for reviewer concerns, or reopening the core method after meta-review. The skill preserves these distinctions rather than treating every failure as a reason to rewrite the paper.

The paper's subset critic compares against the reproduced subset baseline. Table1 describes the full-set comparison against the original SOTA result. A new use of this skill still needs comparable data, protocols and compute: it cannot assume any published scalar is directly comparable to a new run.

The best candidate is selected from successful full-benchmark candidates. In ablation and meta-review refinement, the new state replaces the old state only if result comparison prefers it. Method changes trigger downstream work again. Exhaustion or failure is an allowed termination state.

## Published configuration, not skill defaults

Appendix A, p30 reports:

| Setting | Published configuration |
|---|---|
| General agents | Gemini 3.6 Flash |
| Coding/ablation/rebuttal/draft enhancement | Claude Code with Opus 4.8 |
| Novelty lookup | Two reference papers retrieved via Google Search |
| Limitation extraction | At most 16 rounds |
| Idea experimentation | Two candidates per round: one seed and one evolved idea |
| Experimentation limit | Up to four rounds; stop early at four successful ideas |
| Engineering | At most two rounds |
| Ablation-driven refinement | At most once |
| Simulated peer review | At most two rounds; stop early at ScholarPeer score 8 |
| Review-based refinement | At most once |
| Draft format | ICLR 2025, following PaperOrchestra |

These settings describe the reported system. They are not mandatory spending, model, formatting or iteration requirements for the skill. The paper's examples of generated role outputs are not a complete original prompt library. This repository does not label reconstructed instructions as original system prompts.

## Evaluation and scope of the reported evidence

All numbers here are **authors' reported results**, not reproductions by this repository.

- Table3, p12: 107 input problems: 38 NeurIPS2025, 5 ICLR2026 and 64 ICML2026 Spotlight. Successful generated outputs: 33, 4 and 49 respectively, totaling **86/107 (80.4%)**.
- Table4, p12: reported relative gains across successful cases average **25.2%**, median **7.7%**. This is not an improvement measured on every one of the 107 inputs or a common absolute metric.
- Table3: generated manuscripts average **7.5±1.3** under ScholarPeer, with **91.9%** simulated acceptance; Stanford reviewer **5.7±0.6**, **72.1%**. Denominator is the 86 generated outputs. ScholarPeer also guides refinement; Stanford is described as held out. Neither number is actual conference acceptance.
- §4.2: idea-evolution and review ablations use the 49 successful ICML-derived tasks. Table7 audit reports **49/49** scores verified, **0/49** specification violations, **0/1,814** hallucinated references and **49/49** method–code alignment for the full configuration. Do not generalize those audit denominators to all 107 problems.
- §4.3, pp15–16: cost analysis on the **33 NeurIPS-derived outputs** reports an average **2–3 days** and **$3,765** including tokens and VMs. Conclusion rounds this to approximately $3,800/task. It is not a cost estimate for using a prompt skill.
- Human evaluation, p16/Table10: 33 NeurIPS-derived manuscripts, 9 experienced reviewers. It provides a separate human assessment, not official venue decisions.
- Appendix B's comparison with AutoSOTA concerns differences in task setup and methodological versus configuration changes. It is not evidence that all forms of tuning are invalid research.

## Limits and editorial safeguards

The authors explicitly acknowledge that the system does not consistently achieve spotlight/oral-level conceptual breakthroughs and that cost limits access (p18). Additional interpretation limits here: selected paper-derived empirical tasks are not all scientific domains; relative gains across heterogeneous metrics need care; an evaluator used in optimization is not an independent validator; a favorable self-review does not establish truth. A role sequence performed by one model has no demonstrated equivalence to the reported multi-agent runtime.

The skill adds explicit experiment provenance fields, verification-status reporting, budget selection, and permission boundaries to make a portable instruction set usable. These are editorial operational choices, not claims of verbatim author instructions. Scope is deliberately limited: no forced number of agents, specific vendor model, automatic paper submission, guaranteed SOTA, or universal scoring threshold.

## Reusable archive coverage

[Full native text](../paper/fulltext.md), page records, OCR supplement, machine-detected tables and exact text sources cover the pinned PDF and source release. Appendix C includes limitation/idea/evaluation/ablation/critic/audit/rebuttal artifacts; Appendix D includes the generated DynaSpec-RAG manuscript. These are examples of system outputs, not proof that the released paper contains every agent's complete prompt or full execution history. OCR is uncorrected and formulas/tables must be checked against the PDF or source.
