# ScientistTwo research discipline

Turn a research problem into testable hypotheses, reproducible experiments, and claims supported by artifacts. Apply the stages relevant to the user's assignment; a request for an experiment plan does not authorize running a full research campaign. Use existing tools and approved compute. These instructions do not authorize spawning agents, purchasing services, or submitting papers.

## 1. Target a limitation before proposing a method

Identify the strongest relevant baseline, what it cannot do, and the evidence for that limitation. Distinguish a demonstrated failure from a plausible weakness. Check whether the limitation is actionable and whether the proposed mechanism could actually resolve it.

Generate distinct hypotheses rather than cosmetic variants. For each, state the targeted limitation, mechanism, expected measurable effect, and closest prior work. Check novelty against primary sources; record what was searched and what remains uncertain. Do not equate a new name or a small literature sample with novelty.

## 2. Earn the right to scale

Establish the task rules, metrics and directions, data splits, comparison conditions, and available budget. Reproduce the baseline on a representative subset before evaluating a modification on that same subset. Investigate reproduction gaps before attributing gains to a new idea.

Give each evaluated candidate a verdict backed by logs:

- **Good:** sufficient evidence of improvement to justify full-benchmark evaluation.
- **Engineer:** a promising mechanism with a specific diagnosable implementation or tuning issue; propose a bounded repair.
- **Bad:** inferior results, violated task rules, or exhausted repair budget; retain the failure trace and prune it.

Set task-appropriate iteration and compute limits before expanding the search. A subset win is a screening result, not a full-benchmark claim. Compare successful candidates across the relevant datasets and metrics; expose regressions instead of hiding them in one aggregate score.

## 3. Evolve from traces, including failures

Preserve the hypothesis, code revision, configuration, command, outputs, verdict, and critique for each experiment. Use both successful and failed traces to propose the next mechanism. Distinguish a failed hypothesis from a broken run.

Balance refinement of promising ideas with previously untested alternatives. Do not keep polishing the first plausible seed indefinitely. Stop at the agreed budget or success criterion; report an unsuccessful search honestly.

## 4. Let ablations change the method

For the best validated candidate, design executable component-level comparisons that test where the gain comes from. Keep comparison conditions aligned. Separate component contribution from extra compute, data, tuning, or altered evaluation.

Remove or revise unsupported components when the results warrant it. Keep the previous best artifact until a revised version is verified to improve the relevant outcome. A structural change invalidates affected downstream results: rerun the necessary evaluation and ablations before updating claims.

## 5. Answer criticism with evidence

Draft from the validated method, benchmark results, and ablations. Turn substantive reviewer concerns into targeted experiments or explicit limitations. Do not substitute persuasive rebuttal prose for an experiment that has not run.

Reassess the whole argument after revision. If feedback changes the underlying method, return to evaluation and ablation before redrafting. Treat simulated review as diagnostic feedback; a favorable score is neither real acceptance nor proof of correctness.

## 6. Audit the claim–artifact chain

Before presenting research as verified, check four distinct links:

- **Scores:** reported values match saved outputs; rerun the relevant commands when verification is in scope. Mark results not rerun as unverified.
- **Specification:** implementation follows the task rules; discard gains from leakage or reward hacking.
- **References:** cited works exist and support the attributed statements.
- **Method–code alignment:** the written algorithm matches what the evaluated code actually executes.

Deliver the best verified state with reproduction instructions, results and provenance, failed or negative findings that affect interpretation, remaining limitations, and the precise verification performed. If an experiment was only planned or blocked, say so.

## Source and deeper detail

Adapted from Nam et al., *ScientistTwo*, arXiv:2609.19644v1 (CC BY 4.0). Consult [the evidence map](references/paper-evidence.md) when checking a rule's origin or distinguishing this adaptation from the paper. Use [the cached paper index](paper/README.md) for exact text, tables, appendix artifacts and offline lookup; do not reload the whole archive into context by default.
