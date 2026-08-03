# Data and code for: Local relief and hybrid obstruction in delayed anti-aggregate quantized collective-control systems

Version: v1.0.12

Author: Bongkeun Song  
Affiliation: Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU), Germany
ORCID: 0009-0008-3120-8126

This repository archive supports the manuscript:

**Local relief and hybrid obstruction in delayed anti-aggregate quantized collective-control systems**

## License

Code in `code/` is licensed under MIT (`LICENSE`). Data, figures, tables, manuscript files, and supplements are licensed under CC BY 4.0 (`LICENSE-DATA.md`).

## Scope

The archive contains code, processed data, table-supporting files, final figure image files, supplements, and source-audit materials for the fixed simulation study reported in the manuscript.

The archive is a manuscript-supporting research package focused on local relief, hybrid obstruction, and fixed-implementation structural audit. Controller design, validation, independent plant transfer, universal T3 guarantees, and unconditional global RMSE theory are outside this release scope.

## Layout

- `manuscript/`: manuscript source files used for the submission package.
- `supplements/`: Supplement S1-S3.
- `figures/`: manuscript figures and high-resolution figure files.
- `data/final_structural_audit/`: stream-separated common-random-number q/vote/path audit outputs and table-specific CSV files.
- `data/base_condition_cluster_reanalysis/`: base-condition clustered interaction-model outputs.
- `data/frozen_engine_equivalence/`: fixed-engine equivalence and final-gate audit outputs.
- `data/reduced_order_falsification/`: reduced-order model comparison, held-out prediction files, and freeze-source evidence.
- `data/theory_audit/`: replay/audit values and source files for proof-oriented observability checks.
- `code/analysis/`: package-relative scripts for regenerating or checking the reported analysis outputs.
- `code/fixed_engine_core/`: copied fixed-engine source used for implementation lineage and q=8 reproducibility context.
- `metadata/`: public manifests, figure mapping, DOI audit, and package-integrity records.

## Reproducibility Boundary

The processed outputs used by the manuscript are already included. Some scripts regenerate deterministic audit outputs from the archived implementation and settings; running those scripts is optional and will write package-relative outputs.

This release package preserves the fixed simulation outputs and archived analysis settings; it introduces zero simulations, model refits, threshold tuning, additional gates, or T3 optimisation steps.

## v1.0.12 Changes From v1.0.11

- Manuscript source replaced with the current submission text (`manuscript/t3main_IJGS_submission_layout_repair_v53.docx`), which corrects a duplicate Section 2.1 heading, restores three inline equations that had regressed to plain text, adds an explicit definition of "obstruction channel," numbers the previously unnumbered subsections in Sections 3 and 7, and removes an unsupported "representative design" framing from the final structural audit's parameter panel (Table 7).
- `metadata/reference_doi_full_audit_v53.csv` adds two entries (Vicsek et al. 1995; Acebron et al. 2005) that were cited in the manuscript's Section 2.1 but were missing from the v41 audit; both are verified against independent secondary sources rather than a direct Crossref API call (see the accompanying `.md` for detail).
- Added `LICENSE` (MIT, code) and `LICENSE-DATA.md` (CC BY 4.0, data/figures/manuscript/supplements).
- `CITATION.cff` corrected to use proper German diacritics in the affiliation name and adds an ORCID identifier.
