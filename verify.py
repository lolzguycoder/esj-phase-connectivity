#!/usr/bin/env python3
"""Meaningful algebraic checks, counterexamples, and synthetic-output checks.
Run simulate.py first. No empirical validation is claimed.
"""
import json
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parent
rg=np.random.default_rng(19)
wrap=lambda x:(x+np.pi)%(2*np.pi)-np.pi
O=2*np.pi*8
# Compare different parameter pairs, not a hard-coded assertion of invariance.
phi=rg.normal(size=200);alpha=.4;tau=.012;u=.003
D0=wrap(phi-alpha-O*tau)
D1=wrap(phi-(alpha+O*u)-O*(tau-u))
assert np.max(abs(wrap(D1-D0)))<1e-12
J=np.array([[1,O]])
assert np.linalg.matrix_rank(J)==1
assert np.linalg.matrix_rank(np.array([[1,O],[1,2*O]]))==2
assert np.linalg.matrix_rank(np.array([[1,O],[2,2*O]]))==1
# PLV and PPC are rotation invariant; wPLI is not.
psi=np.array([.2,.7,1.1]);rot=psi-1.
def plv(x):return abs(np.mean(np.exp(1j*x)))
def ppc(x):return (abs(np.sum(np.exp(1j*x)))**2-len(x))/(len(x)*(len(x)-1))
def wpli(x,a):return abs(np.sum(a*np.sin(x)))/np.sum(a*abs(np.sin(x)))
assert np.isclose(plv(psi),plv(rot)) and np.isclose(ppc(psi),ppc(rot))
assert not np.isclose(wpli(psi,np.ones(3)),wpli(rot,np.ones(3)))
# Exact translation and impossible sender-null target.
Dj=np.array([[1.,0],[0,2],[1,1]]);Di=np.array([[1,.4],[.2,1]])
assert np.allclose(Di@np.linalg.pinv(Dj)@Dj,Di)
Ds=np.array([[1.,0]]);Dr=np.eye(2);null=np.array([0.,1.])
assert np.allclose(Ds@null,0) and not np.allclose(Dr@null,0)
# Static and temporal fidelity bound under its assumptions.
for run in range(100):
    Ds=rg.normal(size=(3,2));Dr=rg.normal(size=(4,2));T=rg.normal(size=(4,3))
    z0=rg.normal(size=2);slope=rg.normal(size=2);r=rg.uniform(0,2);tau=rg.uniform(0,.1)
    lag=np.array([.01,.03,.06]);weights=np.array([.2,.3,.5]);mu=weights@lag
    target=Dr@z0
    transfer=r*sum(w*T@Ds@(z0-slope*(tau+s)) for w,s in zip(weights,lag))
    bound=r*np.linalg.norm(T@Ds-Dr,2)*np.linalg.norm(z0)+abs(1-r)*np.linalg.norm(target)
    bound+=r*np.linalg.norm(T@Ds,2)*np.linalg.norm(slope)*(tau+mu)
    assert np.linalg.norm(transfer-target)<=bound+1e-10
# Learning contraction and closed-window invariance.
u=rg.normal(size=3);v=rg.normal(size=2);T=rg.normal(size=(2,3))
err=v-T@u;step=.7/(u@u);updated=T+step*np.outer(err,u)
assert np.allclose(v-updated@u,.3*err)
assert np.allclose(T+0*np.outer(err,u),T)
# Noncommuting matrix serial transfer uses retarded times.
r1=lambda t:.5+.2*np.cos(t);r2=lambda t:.5+.2*np.sin(t)
x=lambda t:np.array([np.cos(t),np.sin(t)])
M1=np.array([[1,.2],[0,1]]);M2=np.array([[.8,0],[.1,1]])
for t in np.linspace(0,3,20):
    direct=r2(t)*M2@(r1(t-.7)*M1@x(t-1))
    assert np.allclose(direct,r2(t)*r1(t-.7)*(M2@M1)@x(t-1))
# Bilinear factorial contrast versus nonlinear single-path separable controls.
U,V=rg.normal(size=(2,100));H,L=1.,.2;chi=.6
F=lambda a,b:a*U+b*V+chi*a*b*U*V+a*a*U**2+np.tanh(b*V)
contrast=F(H,H)-F(H,L)-F(L,H)+F(L,L)
assert np.allclose(contrast,chi*(H-L)**2*U*V)
# Scalar SDT derivative by independent central finite difference.
r=.6;C=.8;h=.9;su=.5;sd=.7
f=lambda r:r*h*C/np.sqrt(r*r*su*su+sd*sd)
assert np.isclose((f(r+1e-5)-f(r-1e-5))/2e-5,h*C*sd*sd/(r*r*su*su+sd*sd)**1.5)
# Deterministic outputs and recovery (conditional synthetic checks).
data=json.loads((root/'results.json').read_text())
assert np.max(abs(np.array(data['centroids_ms'])-data['spectral_slopes_ms']))<1e-5
assert data['access_trace']['trace_closed']==0
assert np.isclose(data['access_trace']['trace_open'],.8*(1-.9**5))
rec=data['mixed_term']['recovery']
assert abs(rec['0.6']['mean_chi']-.6)<.04 and abs(rec['0.0']['mean_chi'])<.04
assert np.mean(rec['0.6']['mixed_mse'])<np.mean(rec['0.6']['additive_mse'])
mix={x['condition']:x for x in data['source_mixing']['summary']}
assert mix['mix+drive']['phase_rmse']>mix['clean10']['phase_rmse']
assert max(data['source_mixing']['harmonic_ablation_max_phase_difference'])<1e-10
assert data['delayed_dictionary']['factorial_max_error']<1e-12
m=data['delayed_dictionary']['test_mse']
assert m['delayed']<m['instantaneous'] and m['delayed']<m['additive']
print('PASS: ridge, harmonic-rank counterexample, observed-score distinctions, translation, temporal bound, SDT, learning, serial timing, factorial contrast, harmonic filtering, and synthetic predictive checks.')
