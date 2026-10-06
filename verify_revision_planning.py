#!/usr/bin/env python3
"""Conditional power planning and analytic revision checks; no empirical fit."""
import json
from pathlib import Path
import numpy as np
from scipy.stats import t,nct,norm,chi2
from numpy.polynomial.legendre import leggauss

def paired_power(n,d,alpha=.025):
 c=t.ppf(1-alpha/2,n-1)
 return float(nct.sf(c,n-1,d*np.sqrt(n))+nct.cdf(-c,n-1,d*np.sqrt(n)))
def minimum(fn,target):
 return next(n for n in range(3,3001) if fn(n)>=target)
# Integrate over the independent sample variance under a normal zero-mean contrast.
z,w=leggauss(600); u=(z+1)/2; w=w/2
def equivalence_power(n,margin=.3,alpha=.025):
 s=np.sqrt(chi2.ppf(u,n-1)/(n-1))
 a=np.sqrt(n)*margin-t.ppf(1-alpha,n-1)*s
 return float(w@np.maximum(2*norm.cdf(a)-1,0))
planning=[{'effect_d':d,'n_80':minimum(lambda n:paired_power(n,d),.8),'n_90':minimum(lambda n:paired_power(n,d),.9)} for d in [.3,.5,.8]]
eq={str(p):minimum(equivalence_power,p) for p in [.8,.9]}
B=np.array([[0.,2.],[.4,0.]])
q=np.array([np.sqrt(5),1.]); c=float(np.max(B@q/q))
assert np.isclose(c,np.sqrt(.8)) and c<1 and B.sum(1).max()==2
rng=np.random.default_rng(6102027); checks=[]
for _ in range(100):
 b=rng.uniform(0,1,(4,4)); np.fill_diagonal(b,0)
 b*=rng.uniform(.1,.95)/max(abs(np.linalg.eigvals(b)))
 weights=np.linalg.solve(np.eye(4)-b,np.ones(4))
 contraction=float(max(b@weights/weights)); assert weights.min()>0 and contraction<1
 checks.append(contraction)
# Non-uniform processing: causal exponential; asymptotic sharpness of 1/2.
mu=.015; om=1e-3/mu; H=1/(1+1j*om*mu)
ratio=float(abs(H-np.exp(-1j*om*mu))/(.5*om**2*mu**2))
assert .999<ratio<=1
# Pointwise bound over gamma shape/scale and frequency choices.
for _ in range(2000):
 shape=rng.uniform(.2,8); scale=rng.uniform(.0001,.02); om=rng.uniform(0,1000)
 h=(1+1j*om*scale)**(-shape); mean=shape*scale; var=shape*scale**2
 assert abs(h-np.exp(-1j*om*mean))<=.5*om**2*var+1e-12
result={'scope':'assumed normal independent replication units; no measured effect size or biological validation','familywise_alpha':.05,'comparisons':2,'per_comparison_two_sided_alpha':.025,'paired_planning':planning,'equivalence_margin_sd':.3,'equivalence_one_sided_alpha':.025,'equivalence_n':eq,'quadrature_nodes':600,'weighted_example':{'row_bound':2,'spectral_radius':float(np.sqrt(.8)),'weights':q.tolist(),'contraction':c},'random_weighted_checks':100,'nonuniform_dispersion_checks':2000,'exponential_small_frequency_ratio':ratio,'seed':6102027}
Path('revision_planning_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
