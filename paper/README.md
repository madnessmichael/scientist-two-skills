# ScientistTwo — reusable paper archive

**Pinned source:** [arXiv:2609.19644v1](https://arxiv.org/abs/2609.19644v1), submitted 17 September 2026. The PDF header also shows 18 September; the identifier/version is the archive key. Attribution and license: [ATTRIBUTION.md](ATTRIBUTION.md).

The archive covers **all 71 physical PDF pages**, not just the abstract or main method. Native extraction contains 241,434 characters. Every page also has an OCR supplement to capture text inside rasterized appendix artifacts. OCR is machine output, not corrected transcription.

| Artifact | Purpose |
|---|---|
| [fulltext.md](fulltext.md) | Human-readable text, grouped by PDF page; C0 controls removed from this view |
| [pages.jsonl](pages.jsonl) | Native text, reading-order variant, text block bounding boxes and page dimensions; original extracted controls preserved |
| [ocr_pages.jsonl](ocr_pages.jsonl) | Separate full-page OCR; useful for image-based reports and tables |
| [ocr_manifest.json](ocr_manifest.json) | OCR engine/settings, render hashes in page records, output hash |
| [tables.json](tables.json) | 67 machine-detected table candidates, cells and page coordinates; not 67 verified semantic tables |
| [structure.json](structure.json) | PDF bookmarks and larger text spans |
| [source/](source/) | 35 source text files: TeX, bibliography and class; preserves exact source equations and table markup |
| [source_environments.json](source_environments.json) | 72 source-environment matches, including figures, tables, equations and listings; can include commented source |
| [manifest.json](manifest.json) | Version, source URLs, source/export SHA-256 hashes and extraction coverage |
| [Evidence map](../references/paper-evidence.md) | Interpreted research mechanisms, configurations, result denominators and adaptation decisions |

PDF-native extraction alone is insufficient: pages **44, 52, 53, 54** contain fewer than 100 native characters, while other appendix pages also contain substantial image text. OCR supplements every page. Do not trust OCR to resolve exact numeric cells or mathematical notation. The full PDF, source archive, extracted source assets, 56 embedded images and all 71 rendered pages are retained in the complete local/Spark cache.

## Read offline

From the repository root, with Python 3 (standard library only):

```sh
python3 scripts/read_paper.py --stats
python3 scripts/read_paper.py --pages 6-9
python3 scripts/read_paper.py --search "engineering" --limit 5
python3 scripts/read_paper.py --ocr --search "variance" --limit 5
python3 scripts/read_paper.py --ocr --pages 44
```

Use native text first, OCR when content is inside images, then the cached PDF/TeX for exact forms. Do not feed the complete archive into every agent context; retrieve the relevant pages.

## Build or verify the complete cache

The first extraction uses `requests` and `PyMuPDF` (recorded version 1.26.7); OCR uses Tesseract (exact engine in OCR manifest). Install these in an isolated environment if rebuilding. The checked-in text archive already works without these dependencies.

```sh
python3 scripts/cache_paper.py --render-all
python3 scripts/ocr_paper.py
```

Sources are downloaded sequentially once, with a delay. Existing source files are reused. With an existing manifest, the first command verifies checked-in export hashes and returns **zero network requests**. Use `--reextract` only to rebuild exports from the cached source files; absent source files may be fetched. Rerunning OCR reuses per-page OCR caches.

Heavy binary assets are in `.cache/` and excluded from Git. A fresh clone contains the extracted text and source text, but must fetch the binary sources once if the complete cache is needed. Source hashes identify the exact cached release; future arXiv revisions are not silently substituted.

No experiment from the paper is executed by these scripts. The archive is complete as source capture plus machine extraction, not a claim of perfect semantic transcription of every figure or a reproduction of the research system.
