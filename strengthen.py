#!/usr/bin/env python3
"""Exact stable-return illustration and independent precision planning; synthetic."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import solve_discrete_lyapunov
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
P=Path(__file__).resolve().parent
A=np.array([[.65,1.2],[0,.65]]);p0=np.array([0.,1.]);v=np.array([1.,0.]);G=solve_discrete_lyapunov(A.T,np.eye(2))
assert np.allclose(G-A.T@G@A,np.eye(2))
q=float(np.sqrt(1-1/np.linalg.eigvalsh(G).max()));limit=float(v@np.linalg.solve(np.eye(2)-A,p0))
inc=np.array([np.linalg.matrix_power(A,k)@p0 for k in range(101)]);partial=np.cumsum(inc@v);tail=abs(limit-partial)
factor=float(np.sqrt(v@np.linalg.solve(G,v))*np.sqrt(p0@G@p0));bounds=factor*q**(np.arange(101)+1)/(1-q)
assert np.all(tail<=bounds+1e-12)
cross=int(np.flatnonzero(partial>=5)[0]);assert cross==4
n=int(np.ceil(4*(norm.ppf(1-.05/(2*4))+norm.ppf(.8))**2/.5**2));assert n==179
out={'scope':'synthetic exact model and illustrative planning, not empirical validation','A':A.tolist(),'p0':p0.tolist(),'readout':v.tolist(),'spectral_radius':float(max(abs(np.linalg.eigvals(A)))),'euclidean_norm':float(np.linalg.norm(A,2)),'lyapunov_G':G.tolist(),'q_G':q,'readout_limit':limit,'partial_sums':partial.tolist(),'increment_norms':np.linalg.norm(inc,axis=1).tolist(),'actual_tail':tail.tolist(),'tail_bound':bounds.tolist(),'first_crossing_index':cross,'first_crossing_ms':18+30*cross,'factorial_planning':{'family_size':4,'alpha':.05,'power':.8,'D_over_sigma':.5,'trials_per_cell':n}}
(P/'strengthening_results.json').write_text(json.dumps(out,indent=2)+'\n')
f,ax=plt.subplots(1,3,figsize=(10,3.2),constrained_layout=True)
ax[0].step(18+30*np.arange(11),partial[:11],where='post');ax[0].axhline(5,color='black',ls='--');ax[0].scatter([138],[partial[4]],color='#d1495b');ax[0].set(xlabel='Arrival time (ms)',ylabel='Projected partial sum')
ax[1].plot(np.arange(16),np.linalg.norm(inc[:16],axis=1));ax[1].axhline(1,color='gray',ls='--');ax[1].set(xlabel='Return index',ylabel='Increment vector norm')
ax[2].semilogy(np.arange(60),tail[:60],label='Actual tail');ax[2].semilogy(np.arange(60),bounds[:60],label='Certified bound');ax[2].set(xlabel='Checked return index',ylabel='Projected tail');ax[2].legend(fontsize=8)
f.savefig(P/'figure_nonnormal.pdf');plt.close(f)
f=plt.figure(figsize=(6,4.5));ax=f.add_subplot(111,projection='3d')
plane=[[-1,-1,0],[1,-1,0],[1,1,0],[-1,1,0]];ax.add_collection3d(Poly3DCollection([plane],alpha=.25,facecolor='#277da1'))
for vec,label,color in [(np.array([1.,0,0]),r'$e_1$','#277da1'),(np.array([0,1.,0]),r'$e_2$','#277da1'),(np.array([0,0,1.]),r'$Q\mathcal{B}(e_1,e_2)$','#d1495b')]:
 ax.quiver(0,0,0,*vec,color=color,arrow_length_ratio=.12);ax.text(*(vec*1.12),label,color=color,fontsize=10)
ax.text(-.85,-.85,0,r'Additive space $S$');ax.set(xlim=(-1,1.4),ylim=(-1,1.4),zlim=(0,1.4),xlabel='Receiver 1',ylabel='Receiver 2',zlabel='Innovation');ax.view_init(elev=23,azim=-48);f.savefig(P/'figure_innovation_geometry.pdf',bbox_inches='tight');plt.close(f)
print('Stable return certificate verified; threshold index',cross,'; illustrative factorial n=',n)
