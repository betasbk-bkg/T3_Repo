# Reference DOI Full Audit v53

## Verdict

`REFERENCE_DOI_FULL_AUDIT_53_ENTRIES_CROSSREF_API_PLUS_2_ENTRIES_SECONDARY_SOURCE`

## Scope

- DOI entries audited: 55
- Entries verified via direct Crossref/DataCite API call: 53 (index 1-53, inherited from v41 audit, unchanged)
- Entries verified via independent secondary sources only: 2 (index 54-55, added when the manuscript adopted the Vicsek/Kuramoto system-class positioning)
- Entries with no flags: 55
- Entries with flags: 0

## New Entries (index 54-55)

Added to the reference list to support the system-class positioning discussion (Section 2.1). Both were verified against the following independent secondary sources rather than a direct Crossref API call, because the Crossref API was not reachable in the verifying session:

- **Acebron et al. 2005** (`10.1103/RevModPhys.77.137`): confirmed via the publisher page (APS, Rev. Mod. Phys. 77, 137, published 7 April 2005), Semantic Scholar, and BibSonomy bibtex record. Title, authors, volume/issue/pages, and DOI match the manuscript entry exactly.
- **Vicsek et al. 1995** (`10.1103/PhysRevLett.75.1226`): confirmed via PubMed, NASA ADS, and BibSonomy bibtex record. Title, authors, volume/issue/pages, and DOI match the manuscript entry exactly.

Both entries carry `flag = OK_not_direct_crossref_api` in the CSV to distinguish this weaker verification method from the direct-API method used for entries 1-53. If a direct Crossref/DataCite API check becomes available, re-running it for these two DOIs would close this distinction.

## Inherited Repair (from v41 audit)

The Lin and Ling reference entry was updated to a 2025 bibliographic year because Crossref reports DOI `10.1109/TAC.2024.3422230` as published in 2025 with volume `70`, issue `1`, and pages `697-704`. The manuscript still cites the same DOI and title.
