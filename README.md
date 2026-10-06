# ESJ structure-preserving revision

The manuscript retains the eight-section architecture, dictionary/translation model, projection/alignment/completion framework, bilinear interaction, and learning postulate. Mathematical and behavioral claims are qualified by explicit models.

Open `main.tex` in Overleaf; upload the complete ZIP. The project includes the ESJ class, logo, bibliography, generated macros, figures, main PDF, supplement, and editorial response.

## Numerical reproduction

Use Python 3.12 with `python -m pip install -r requirements.txt`, then `python reproduce.py`. This runs the supplied legacy simulation and verifier in their own directory, the revised simulation, independent checks, and macro generation. Generated PDFs can differ bytewise due to metadata; compare numeric JSON outputs. Revised code and figures use alpha for receptive center, matching the manuscript; original legacy files remain unchanged.

## LaTeX build

Run `pdflatex main`, `bibtex main`, `pdflatex main` twice, then `pdflatex supplement` and `pdflatex response` twice each. The main auxiliary file provides cross-references for the supplement and response.

## Limits

Synthetic verification establishes internal consequences, not biological validation. Original files are retained under legacy_supplied for provenance; original response claims are not endorsed. The public project repository is https://github.com/lolzguycoder/esj-phase-connectivity and the author-supplied project DOI is https://doi.org/10.5281/zenodo.23165931. Correspondence between that archive and this exact revision could not be independently verified. The attached response maps only the editorial concerns supplied in this conversation. Author review and journal formatting/reference checks remain required.

## Projection theorem revision

Theorem 1 now states when a nonzero item projection establishes modeled sender-to-receiver communication and derives the exact source-content contrast at fixed phase. The completion criterion is a separate corollary. The supplement and independent verifier include randomized contrast checks and a temporal-cancellation counterexample. The manuscript author-contribution statement was shortened as requested.

## Integrated scientific development

The main manuscript adds uncertainty-certified communication, an effective bilinear interaction rank criterion, a full-rank carrier/gain design, and a gain-weighted expected-learning result. A proposed integrated experiment distinguishes structural support, gain, nonlinear content integration, and learning. The independent verifier adds random bilinear rank tests and exact finite-distribution learning checks. Existing empirical limitations and the no-experience-variable scope remain. New algebraic results do not establish a biological breakthrough.

## Full-proof edition

All fifteen main-text proofs are expanded, including the linear extension construction, temporal norm bound, likelihood and information factorization, exact threshold cases, harmonic null spaces, observation-kernel argument, sender-contrast result, attained first-passage conditions, robust map bounds, sensitivity derivatives, factorial cancellation, interaction quotient-rank proof, and expected-learning spectral dynamics. The supplementary interaction proof is also expanded. Gain continuity, positive concentration for inverse windows, and initial-error integrability are explicitly stated where needed. The current expanded revision is 53 manuscript pages, 14 supplementary pages, and 4 editorial-response pages.

## Readability edition

The eight-section structure and all prior full proofs remain. A roughly 196-word abstract, section reading guide, vector roadmap, explicitly complementary behavioral/geometric models, and a worked two-coordinate learning example improve navigation. The new unexcited-direction corollary has a full proof. Revised source and recovery figures use alpha consistently; regression beta coefficients are distinct. Table 3 uses ragged-right columns and explicit row spacing, and the sensitivity display labels the two independent noise sources.

`make_reader_figures.py` regenerates the roadmap and exact learning curves. `reader_results.json` stores the worked example. The complete driver regenerates ten revised figures, runs independent checks, and rebuilds macros. All pre-existing numerical results matched exactly after notation migration. The main paper has 34 pages in the journal submission format; supplement 8; response 3.

## Reciprocal projection and latency edition (6 October 2026)

The eight-section manuscript now closes the calibrated directed transfers into one stable reciprocal model. Full proofs derive the delayed matrix echo series, item-specific return support, a positive-channel threshold latency, and preservation of the stationary two-edge parameter ridge. Independently anchored onsets and resolved returns can provide a separate timing constraint. Nonzero projection alone does not establish finite completion or measured brain communication.

`reciprocal.tex` is included by `main.tex` and must remain beside it. `simulate_reciprocal.py` generates `figure_reciprocal.pdf` and all illustrative values in `reciprocal_results.json`. The driver now regenerates eight revised figures. `verify.py` independently compares 100 random stable matrix pairs with a direct delayed two-population recurrence, checks threshold limits and readout rotation, and checks 100 compensated two-edge carrier responses. Supplement S14 gives all units, parameters, counterexamples and reproduction settings.

The 60 ms extra waiting term in the worked example is accumulation over two 30 ms round trips, in addition to an 18 ms direct arrival. It is a conditional model prediction, not an overlooked physiological delay established by these data. The prefrontal/contralateral application is proposed, supported by independently referenced motivation, and has no empirical validation here. The exact local revision has not been published to the named repository or verified against the cited DOI.

Final compiled reciprocal revision: manuscript 40 pages; supplement 9; editorial response 3. All reference and citation checks clean; no overfull boxes. Full reproduction completed successfully, with 16 independent verification groups.

## Latest editorial revision and public-data screen

The title now emphasizes phase-gated interregional transfer. Retarded processing and discrete delays are unified as one operator model and its instantaneous-memory limit. `general_returns.tex` supplies non-invariant first-passage bounds; `rank_sensitivity.tex` links innovation rank to an explicit Gaussian decision model. The first two access subsections are merged. Symbols are defined locally.

`compare_mse.py` adds 300 independent full-series paired comparisons, pointwise Student intervals and four-test Holm adjustment. `mse_comparison_results.json` retains every model MSE and selected lag. The full driver executes this analysis; the mathematical verifier now has 19 check groups.

`dataset_review/PUBLIC_DATA_REVIEW.md` compares public datasets with the actual model requirements. All 74 public CCEP electrode tables were downloaded and screened; one has explicitly bilateral contacts, and its event metadata contain stimulation from both hemispheres. This is metadata feasibility only. No neural waveform or behavioral trial was fitted. The online metadata screen is optional and separate from numerical reproduction, so `reproduce.py` needs no network access.

## Detailed final review revision

The current source adds `stable_returns.tex` (a full Schur-stable non-normal return proof), `experimental_design.tex` (minimal design and hypothetical precision planning), `comparison_positioning.tex`, and `supplementary_revision.tex` (glossary, gate choice and two new figures). Run `python strengthen.py` for the added exact illustrations; it is included in `reproduce.py`. `DEEPSEEK_REVISION_CHECKLIST.md` maps the detailed comments to changes and identifies mathematically incorrect suggestions that were corrected rather than copied. Public data remain feasibility candidates: no neural waveform was fitted, and no single inspected release validates the full model.

## Nervous-system extension (6 October 2026)

The Enosh manuscript remains `main.tex`. Added files are `nervous_network.tex`, `nervous_empirical.tex`, `verify_nervous_network.py`, `nervous_network_results.json`, `figure_nervous_network.pdf`, and `NERVOUS_SYSTEM_EVIDENCE.md`. Supplement S19 explains the checks. Run the standalone verifier or the full driver. All new numerical evidence is synthetic; public resources are assessed as empirical candidates. No claim of a biological breakthrough is established by these checks.

Figure export uses buffered PDF writes in the reciprocal script and the legacy figure helper; the retained numerical models and seeds are unchanged.

## Final minor revisions

`verify_revision_planning.py` and `revision_planning_results.json` reproduce the weighted stability example, randomized comparison matrices, gamma-kernel bounds, and assumed-effect paired-MSE and equivalence-power calculations. Supplement S20 specifies all assumptions. The full numerical driver includes these checks. The Dryad file manifest and published simultaneous-area coverage transcription are included under `dataset_review/`. They support eligibility screening, not biological model validation. The public release has no listed dlPFC–M1 simultaneous session and only nine PMd–dlPFC candidate sessions across two animals. Supplementary Figure S9 is included in S17.
