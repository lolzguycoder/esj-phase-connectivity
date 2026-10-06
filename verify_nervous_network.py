#!/usr/bin/env python3
"""Independent finite-time graph and causal-processing checks; no empirical fit."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
SEED=6102026
rng=np.random.default_rng(SEED)
errors=[]
for run in range(100):
    n,p,T=4,2,51; edges=[]
    for i in range(n):
        for j in range(n):
            if i!=j and rng.random()<.55:
                L=rng.normal(size=(p,p));L*=.15/max(1,np.linalg.norm(L,2))
                edges.append((i,j,int(rng.integers(4,10)),L,rng.dirichlet(np.ones(3))))
    b=np.zeros((T,n,p));b[:,0,:]=rng.normal(size=p);direct=b.copy()
    for t in range(T):
        for i,j,lag,L,h in edges:
            for s,weight in enumerate(h):
                if t>=lag+s:direct[t,i]+=weight*(L@direct[t-lag-s,j])
    def K(x):
        out=np.zeros_like(x)
        for i,j,lag,L,h in edges:
            for s,weight in enumerate(h):
                d=lag+s;out[d:,i]+=weight*(x[:-d,j]@L.T)
        return out
    term=b.copy();series=b.copy()
    for m in range(T//4+1):term=K(term);series+=term
    errors.append(float(np.max(np.abs(direct-series))))
assert max(errors)<1e-12
# The vector route maps are composite maps, including intermediate translations.
t=np.arange(0,41,dtype=float)/1000;d=np.array([1.,0.]);v=np.array([1.,0.])
fast=np.diag([0.,.2]);a=.3*np.eye(2);bmat=-.3*np.eye(2)
cfast=float(v@fast@d);ca=float(v@a@d);cb=float(v@bmat@d)
y=cfast*(t>=.008)+ca*(t>=.012)+cb*(t>=.016)
same=ca*(t>=.012)+cb*(t>=.012)
B=abs(cfast)*(t>=.008)+abs(ca)*(t>=.012)+abs(cb)*(t>=.016)
assert np.all(np.abs(y)<=B+1e-14) and np.all(same==0)
onset=float(t[np.flatnonzero(abs(y)>1e-12)[0]])
assert onset==.012 and max(abs(y))<.4 and y[-1]==0
for k in range(2000):
    a=float(rng.uniform(.0001,.025));mu=a+float(rng.uniform(0,.02));om=float(rng.uniform(0,500))
    H=np.exp(-1j*om*mu)*np.sinc(om*a/np.pi);bound=om**2*(a*a/3)/2
    assert abs(H-np.exp(-1j*om*mu))-bound<1e-12
omega=np.linspace(0,1000,1001);mu=.015;a=.003;tau=.018;u=.006
H=np.exp(-1j*omega*mu)*np.sinc(omega*a/np.pi)
H2=np.exp(-1j*omega*(mu-u))*np.sinc(omega*a/np.pi)
ambiguity=float(np.max(np.abs(np.exp(-1j*omega*tau)*H-np.exp(-1j*omega*(tau+u))*H2)))
assert ambiguity<1e-12 and mu-a>=u
for k in range(2000):
    c=rng.normal(size=10);F=rng.uniform(size=10);r=c@F;upper=abs(c)@F
    assert abs(r)<=upper+1e-12
    for j in range(10):assert abs(r)+1e-12>=2*abs(c[j])*F[j]-upper
results={'status':'PASS','seed':SEED,'scope':'synthetic verification only; no neural data fitted',
 'network_realizations':100,'max_network_response_error':max(errors),'variance_checks':2000,
 'certificate_checks':2000,'supported_onset_ms':onset*1000,'fast_null_route_ms':8,
 'max_distinct_route_readout':float(max(abs(y))),'threshold_never_reached':.4,
 'simultaneous_cancellation_max':float(max(abs(same))),
 'broadband_temporal_ambiguity_max_error':ambiguity,
 'forty_hz_magnitude_halfwidth_2ms':float(abs(np.sinc(2*40*.002))),
 'forty_hz_magnitude_halfwidth_10ms':float(abs(np.sinc(2*40*.010)))}
fast_gain=float(.5*np.exp(2*(np.cos(2*np.pi*40*.005)-1)))
assert fast_gain<.4
results['uncompensated_13ms_amplitude']=fast_gain
results['compensated_13ms_amplitude']=.5
(ROOT/'nervous_network_results.json').write_text(json.dumps(results,indent=2)+'\n')
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(1,3,figsize=(10.8,3.2))
ax[0].step(t*1000,y,where='post',label='Signed target response');ax[0].step(t*1000,B,where='post',ls='--',label='Absolute upper bound');ax[0].axhline(.4,color='gray',ls=':',label='Threshold 0.4');ax[0].axvline(8,color='gray',alpha=.4);ax[0].set(xlabel='Time from source onset (ms)',ylabel='Readout amplitude',title='Supported detour and later cancellation');ax[0].legend(fontsize=7)
ax[1].step(t*1000,ca*(t>=.012),where='post',label='Route A');ax[1].step(t*1000,cb*(t>=.012),where='post',label='Route B');ax[1].plot(t*1000,same,ls='--',label='Observed sum');ax[1].set(xlabel='Time (ms)',title='Nonzero routes, zero observed effect');ax[1].legend(fontsize=7)
freq=np.linspace(0,100,501)
for width in [.002,.010]:ax[2].plot(freq,abs(np.sinc(2*freq*width)),label=f'Half-width {width*1000:.0f} ms')
ax[2].set(xlabel='Frequency (Hz)',ylabel='Temporal factor magnitude',title='Equal mean delay, different dispersion');ax[2].legend(fontsize=7)
fig.tight_layout();fig.savefig(ROOT/'figure_nervous_network.pdf');plt.close(fig)
print(json.dumps(results,indent=2))
