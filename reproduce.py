#!/usr/bin/env python3
"""One-command numerical regeneration; compilation is a separate documented step."""
from pathlib import Path
import subprocess,sys,hashlib,json
p=Path(__file__).resolve().parent
subprocess.run([sys.executable,'simulate.py'],cwd=p/'legacy_supplied',check=True)
subprocess.run([sys.executable,'verify(1).py'],cwd=p/'legacy_supplied',check=True)
for name in ['simulate.py','make_reader_figures.py','simulate_reciprocal.py','compare_mse.py','strengthen.py','verify_nervous_network.py','verify_revision_planning.py','verify.py','build_results.py']:
 subprocess.run([sys.executable,str(p/name)],cwd=p,check=True)
(p/'reproduction_checks.json').write_text(json.dumps({'status':'PASS','commands':['simulate.py','make_reader_figures.py','simulate_reciprocal.py','compare_mse.py','strengthen.py','verify_nervous_network.py','verify_revision_planning.py','verify.py','build_results.py'],'results_sha256':hashlib.sha256((p/'results.json').read_bytes()).hexdigest(),'reciprocal_results_sha256':hashlib.sha256((p/'reciprocal_results.json').read_bytes()).hexdigest(),'mse_comparison_sha256':hashlib.sha256((p/'mse_comparison_results.json').read_bytes()).hexdigest(),'nervous_network_sha256':hashlib.sha256((p/'nervous_network_results.json').read_bytes()).hexdigest(),'revision_planning_sha256':hashlib.sha256((p/'revision_planning_results.json').read_bytes()).hexdigest(),'strengthening_sha256':hashlib.sha256((p/'strengthening_results.json').read_bytes()).hexdigest(),'all_revised_figures':['figure_joint.pdf','figure_delivery.pdf','figure_coverage.pdf','figure_temporal.pdf','figure_escape_mixing.pdf','figure_roadmap.pdf','figure_learning_example.pdf','figure_reciprocal.pdf','figure_nonnormal.pdf','figure_innovation_geometry.pdf','figure_nervous_network.pdf'],'scope':'all revised numerical results; no empirical validation'},indent=2)+'\n')
for figure in [*p.glob('figure*.pdf'),*(p/'legacy_supplied').glob('figure*.pdf')]:
 data=figure.read_bytes()
 if not data.startswith(b'%PDF-') or b'%%EOF' not in data[-2048:]:
  raise RuntimeError(f'Incomplete generated PDF: {figure.name}')
print('All revised numerical outputs regenerated and checked; figure PDFs are complete.')
