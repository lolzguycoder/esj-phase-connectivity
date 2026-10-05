# Revised submission: single-band delay--preference identifiability

Upload this folder to Overleaf and set **main.tex** as the main document. PDFs and all required class/figure files are included. Compile supplement.tex and response.tex separately; compile main.tex first so the response letter can import exact section/page references from main.aux through xr.

## Reproduce

```
python -m pip install -r requirements.txt
python simulate.py
python verify.py
python build_results.py
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
pdflatex supplement.tex
pdflatex supplement.tex
pdflatex response.tex
pdflatex response.tex
```

This revision integrates the supplied ESJ source and the dictionary/translation ideas from the supplied psyArXiv draft. All outputs are synthetic. The main paper contains three figures; supplementary methods contain four secondary figures. No empirical data, conscious-state measurement, unique mechanism identification, or human sample-size justification is claimed.

## Model components

- Regional encoding dictionaries and linear translation, with an exact factorization condition.
- Conduction delay, separate causal processing kernels, phase-dependent arrival gain.
- A constrained bilinear finite-memory interaction between unreported and report-associated pathways.
- Sensitivity distinguished from response criterion, and a separately gated learning trace.
- A theorem conditional on the complete observation law depending on eta = alpha + Omega*tau.

## Verification and limits

verify.py checks algebra, counterexamples, numerical bounds, phase-score distinctions, trace updates, harmonic filtering, and held-out synthetic predictive behavior. results.json contains per-realization coefficient estimates and intervals, mixing ablations, and temporal prediction errors. build_results.py generates the numerical values embedded in main.tex. environmental package versions are recorded in environment.txt.

The finite-memory temporal check is one generated realization with known maps and processing kernels; it does not recover separate conduction and processing biology. Interaction intervals condition on exact features and gains; coverage below nominal is reported. Flexible competitors demonstrate predictive nonuniqueness. A pure 16-Hz harmonic is removed by the specified ideal 6--10 Hz filter. None of these checks is independent biological validation.

## Outstanding public-code requirement

The executable review copy is complete, but it is not a permanent public code deposit. See RELEASE_CHECKLIST.md. The response letter marks Reviewer 1 major comment 2 as **partially fulfilled** until a real public archive URL exists. Do not claim complete reviewer compliance before that deposit.
