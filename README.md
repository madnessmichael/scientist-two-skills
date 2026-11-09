# ScientistTwo Skills

A research skill distilled from **[ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI](https://arxiv.org/abs/2609.19644v1)**, by Nam et al. It brings the paper's experimental discipline into a coding agent: start from an actionable limitation, reproduce a baseline, screen ideas cheaply, learn from failures, and revise claims through experiments.

Inspired by the compact instruction format of [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills). This is an independent, AI-assisted adaptation, with a [rule-by-rule evidence map](references/paper-evidence.md) and a reusable archive of the full paper.

## The skill

| Principle | What changes in practice |
|---|---|
| **Limitations before methods** | Connect each hypothesis to a demonstrated baseline weakness and check related work. |
| **Earn the right to scale** | Reproduce a subset baseline; decide **Good / Engineer / Bad** before full-suite compute. |
| **Learn from the whole search** | Preserve failed traces and explore new seeds alongside promising refinements. |
| **Ablations can change the method** | Test where gains come from; retain the previous best until a revision wins. |
| **Rebuttal means experiments** | Resolve substantive criticism with targeted evidence, then update the manuscript. |
| **Audit the claim–artifact chain** | Check scores, task rules, references, and agreement between written method and code. |

Read the complete instructions in **[SKILL.md](SKILL.md)**. [CLAUDE.md](CLAUDE.md) contains the same body without skill frontmatter for environments that load project instructions.

## Use

Clone the repository and make `SKILL.md` available to your agent's skill loader, or explicitly ask the agent to read it before a research task. It is self-contained; supporting references are loaded only when needed. Installation does not require an API key or an experiment runtime.

```sh
git clone https://github.com/madnessmichael/scientisttwo-skills.git
```

Example request:

> Read SKILL.md. Investigate whether retrieval improves our small-model agent on this benchmark. Use the existing baseline and a two-GPU-hour budget. Start with a subset experiment, retain failure traces, and report what the results support. Do not write a paper unless the evidence warrants it.

For a planning-only task:

> Use SKILL.md to critique this hypothesis and propose a baseline, subset screening test and decisive ablations. Do not run experiments.

The skill follows the scope and compute budget of the request. It does not automatically start multiple agents, buy compute, or submit manuscripts. Executing research can still incur model and compute costs; the skill itself sets no spending allowance.

## The paper, cached once

The repository includes an offline text archive of **all 71 pages**, including references, configurations and qualitative appendix artifacts. It contains native page text, full-page OCR, table candidates, exact TeX/bibliography sources, and source hashes. No repeated crawling is needed to search or reread those exports.

```sh
python3 scripts/read_paper.py --pages 6-9
python3 scripts/read_paper.py --search "rebuttal" --limit 5
python3 scripts/read_paper.py --ocr --pages 44
```

See **[the archive index](paper/README.md)** for file descriptions, coverage limitations and cache commands. Large PDF/source binaries, embedded images and rendered pages are cached separately rather than added to Git. A fresh clone can read the exports immediately; rebuilding the binary cache requires a one-time download.

## What the evidence supports

The authors report successful research outputs on **86/107** paper-derived problems. Their system uses specialized agents, repeated code execution and simulated review; its reported average cost is **$3,765** over 33 NeurIPS-derived outputs. These are results of the paper's system, not measured results of this skill. We have extracted and inspected the source; we have **not reproduced the system or benchmark outcomes**. The [evidence map](references/paper-evidence.md) records result denominators, configuration and interpretation limits.

## Source and license

Original paper and attributed paper extracts: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), subject to embedded source-file notices; see [attribution](paper/ATTRIBUTION.md). Original repository tooling and editorial contributions: [MIT](LICENSE). Adaptations are identified; no author affiliation or endorsement is implied.

## Differences from the actual paper

This skill translates ScientistTwo's research decisions into portable instructions. It does **not** implement its multi-agent orchestration, original prompts, execution infrastructure or automated reviewers, and cannot inherit its reported performance. Fixed vendor models, search counts and iteration thresholds become task-specific budgets; explicit provenance and permission boundaries are editorial additions. The [evidence map](references/paper-evidence.md) makes these changes traceable.
