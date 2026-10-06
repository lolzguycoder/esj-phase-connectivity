# Nervous-system extension: evidence and proposed analysis

Checked 6 October 2026. Repository descriptions and papers were inspected; no new biological waveform data were fitted or counted as model validation.

| Source | Role in this revision | Main limitation |
|---|---|---|
| Ford et al. (2015), https://doi.org/10.1038/ncomms9073 | Biological timing motivation | Specialized auditory circuit; not a calibrated content map |
| Binish et al. (2026), https://doi.org/10.1038/s41593-026-02290-4 | PFC–M1 projection motivation | Reported subspaces do not identify this model's isolated causal routes |
| Michaels et al. (2025), https://doi.org/10.1038/s41586-025-09690-9 | Sensorimotor application | Perturbation affects a closed biological system |
| Dryad, https://doi.org/10.5061/dryad.0vt4b8hbr | Proposed empirical follow-up | Raw-session coverage must be established before fitting |
| F-TRACT atlas, https://zenodo.org/records/7015415 | Independent reference candidate | Derived delays are model-dependent |
| PhysioNet EMG v1.0.0, https://doi.org/10.13026/C24S3D | Excluded full-model candidate | Voluntary EMG lacks the required paired-site and population design |

The official Dryad API manifest (version 395374, all three file-list pages) contains 49 MAT session files: 29 monkey M and 20 monkey P. The metadata PDF download returned HTTP 403, and the official API download endpoints returned HTTP 401. Instead, the corresponding paper’s Extended Data Table 1 was inspected directly (page 22 of the author-hosted PDF: https://www.diedrichsenlab.org/pubs/Michaels_Nature_2025.pdf). Its simultaneous-area candidates among S1, M1, PMd, and dlPFC comprise nine PMd–dlPFC, three S1–M1, two M1–PMd, and two S1–PMd sessions. No listed session pairs dlPFC with M1. The restricted manual transcription is in `dataset_review/michaels_paired_coverage.csv`; the complete official archive manifest is in `dataset_review/michaels_file_manifest.json`. Sessions from two animals are not independent animal replications. Additional quality and trial-synchrony screening remains necessary; no raw-waveform fit was performed.

## What is proved

Theorem `thm:network` gives a directed-walk expansion of the constant-gain retarded operator, a lower bound on readout arrival, simultaneous-route cancellation, and conservative threshold certificates. Proposition `prop:dispersion` gives a variance bound for a causal processing kernel and a broadband conduction–processing non-identifiability example. These are conditional mathematical results using classical operator and Fourier methods.

## What is tested

`python verify_nervous_network.py` checks independently implemented network recurrences, signed-route bounds, uniform-delay dispersion, and exact temporal equivalence. `nervous_network_results.json` records all output values and the seed. `python reproduce.py` runs the new checks together with the retained revised analyses.

## What would establish a substantive empirical advance

Freeze maps and readouts independently; verify simultaneous source–target coverage; predict item-specific onset and null contrasts on held-out trials; intervene on the proposed detour; compare identical observed inputs against a flexible delayed rival. Separate conduction, processing, motor mechanics, and sensory transduction with independent timing constraints. Biological confirmation and priority against prior work remain open.

## Final minor revision

Weighted-network stability is proved through the nonnegative edge-norm matrix and a positive diagonal scaling. Non-uniform gamma/exponential dispersion checks and exact conditional paired-t/equivalence planning are reproducible in `verify_revision_planning.py`. All power values are hypothetical planning values, not estimates of effects in the public release.
