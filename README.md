# Data and code for: Local relief without global closure: hybrid obstruction channels in delayed quantized collective control

Version: v1.6.1

Author: Bongkeun Song  
Affiliation: Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU), Germany
ORCID: 0009-0008-3120-8126

This repository archive supports the manuscript:

**Local relief without global closure: hybrid obstruction channels in delayed quantized collective control**

## License

Code in `code/` is licensed under MIT (`LICENSE`). Data, figures, tables, and supplements are licensed under CC BY 4.0 (`LICENSE-DATA.md`).

## Scope

The archive contains code, processed data, table-supporting files, final figure image files, supplements, and source-audit materials for the fixed simulation study reported in the manuscript.

The archive is a manuscript-supporting research package focused on local relief, hybrid obstruction, and fixed-implementation structural audit. Controller design, validation, independent plant transfer, universal T3 guarantees, and unconditional global RMSE theory are outside this release scope.

## Layout

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

## v1.6.1 Changes From v1.6.0

- Archive scope narrowed to data, code, figures, supplements, and metadata: manuscript source files are no longer distributed in this repository archive and are available with the associated submission.
- Supplementary Information S4 (supplementary tables and figures) and S5 (smooth local relief derivation) added to `supplements/`, matching the current submission's supplementary set. The checksum manifest is regenerated accordingly. No data, code, figures, or numerical results were changed.

## v1.6.0 Changes From v1.0.12

- Manuscript source updated to the current submission text: restructured into Introduction/Results/Discussion/Methods order, retitled, related-work discussion condensed into the Introduction, references converted to numbered order-of-appearance style, tables and figures renumbered accordingly, and two typographic omissions of R^2 in the reduced-order comparison text repaired. No data, code, figures, or numerical results were changed.
- Supplement headings harmonized to "Supplementary Information S1/S2/S3" and the S1 cross-reference updated from main-text Table 10 to Table 2 to match the renumbered manuscript. Supplement content otherwise unchanged.
- Repository metadata (CITATION.cff, Zenodo draft, data availability statement) updated to the new manuscript title and this version number.

## v1.0.12 Changes From v1.0.11

- Manuscript source replaced with the then-current submission text, which corrects a duplicate Section 2.1 heading, restores three inline equations that had regressed to plain text, adds an explicit definition of "obstruction channel," numbers the previously unnumbered subsections in Sections 3 and 7, and removes an unsupported "representative design" framing from the final structural audit's parameter panel (Table 7).
- `metadata/reference_doi_full_audit_v53.csv` adds two entries (Vicsek et al. 1995; Acebron et al. 2005) that were cited in the manuscript's Section 2.1 but were missing from the v41 audit; both are verified against independent secondary sources rather than a direct Crossref API call (see the accompanying `.md` for detail).
- Added `LICENSE` (MIT, code) and `LICENSE-DATA.md` (CC BY 4.0, data/figures/manuscript/supplements).
- `CITATION.cff` corrected to use proper German diacritics in the affiliation name and adds an ORCID identifier.
