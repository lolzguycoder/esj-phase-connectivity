#!/usr/bin/env python3
"""Independent algebra, counterexample and output checks; no biological validation."""
from pathlib import Path
import json
import numpy as np
from model import gate,wrap,complex_mean,gate_window,sensitivity,shifted
p=Path(__file__).resolve().parent;rg=np.random.default_rng(20261005);checks=[]
def done(name):checks.append(name)
O=2*np.pi*8;gamma,alpha,tau=.35,.8,.018
psi=np.linspace(-np.pi,np.pi,37);m=complex_mean(psi,O,gamma,alpha,tau);obs=m+.05*(rg.normal(size=37)+1j*rg.normal(size=37))
ll=lambda g,b,t:-np.sum(abs(obs-complex_mean(psi,O,g,b,t))**2)/(.005)
for u in np.linspace(-.01,.015,20):
 assert np.allclose(m,complex_mean(psi,O,gamma+O*u,alpha+O*u,tau-u),atol=1e-12)
 assert abs(ll(gamma,alpha,tau)-ll(gamma+O*u,alpha+O*u,tau-u))<1e-9
done('Full joint mean and Gaussian likelihood ridge')
pars=np.array([gamma,alpha,tau]);cols=[]
for j,step in enumerate([1e-5,1e-5,1e-7]):
 e=np.eye(3)[j]*step;cols.append((complex_mean(psi,O,*(pars+e))-complex_mean(psi,O,*(pars-e)))/(2*step))
D=np.array(cols).T;F=np.real(D.conj().T@D);null=np.array([O,O,-1.]);assert np.linalg.norm(F@null)/np.linalg.norm(F)<1e-7
J=np.array([[1,0,O],[0,1,O]]);J3=np.array([[1,0,O],[1,0,2*O],[0,1,O]]);assert np.linalg.matrix_rank(J)==2 and np.linalg.matrix_rank(J3)==3
phaseJ=np.array([[1.,O]]);assert np.allclose(phaseJ@np.array([O,-1]),0);assert not np.allclose(phaseJ@np.array([1.,-O]),0)
assert np.linalg.matrix_rank(np.array([[1,O],[2,2*O],[3,3*O]]))==1
done('Numerical Fisher null, three-parameter design rank, corrected phase null and harmonic ambiguity')
for _ in range(100):
 om=rg.uniform(1,100,5);w=rg.uniform(.1,2,5);X=np.column_stack([np.ones(5),om]);I=X.T@(w[:,None]*X);wb=w@om/w.sum();assert np.isclose(np.linalg.det(I),w.sum()*np.sum(w*(om-wb)**2))
done('Independent weighted-information determinant')
Dj=np.array([[1.,0],[0,2],[1,1]]);Di=np.array([[1,.4],[.2,1]]);assert np.allclose((Di@np.linalg.pinv(Dj))@Dj,Di)
Ds=np.array([[1.,0]]);Dr=np.eye(2);znull=np.array([0.,1]);assert np.allclose(Ds@znull,0) and not np.allclose(Dr@znull,0)
for _ in range(200):
 Ds=rg.normal(size=(3,2));Dr=rg.normal(size=(4,2));T=rg.normal(size=(4,3));z=rg.normal(size=2);slope=rg.normal(size=2);r=rg.uniform(0,2);tau0=rg.uniform(0,.1);lag=np.array([.01,.03,.06]);w=np.array([.2,.3,.5]);mu=w@lag
 U=r*sum(ww*T@Ds@(z-slope*(tau0+q)) for ww,q in zip(w,lag));bound=r*np.linalg.norm(T@Ds-Dr,2)*np.linalg.norm(z)+abs(1-r)*np.linalg.norm(Dr@z)+r*np.linalg.norm(T@Ds,2)*np.linalg.norm(slope)*(tau0+mu)
 assert np.linalg.norm(U-Dr@z)<=bound+1e-10
done('Factorization, impossible sender-null target and 200 randomized fidelity bounds')
for A in [.1,.25,.5,1.]:
 th=.25;delta=np.linspace(-np.pi,np.pi,5001);passed=A*gate(delta)>=th;theta=gate_window(A,th)
 if theta is None:assert not np.any(passed)
 else:assert np.all(passed==(abs(delta)<=theta+1e-12))
assert gate(np.pi)>0
M=np.diag([1.,0]);v=np.array([1.,0]);z=np.array([0.,1]);assert v@M@z==0 and np.linalg.norm(M@v)>0
for _ in range(100):
 Mhat=rg.normal(size=(3,2));E=rg.normal(size=(3,2));E=E/np.linalg.norm(E,2)*.08;z=rg.normal(size=2);v=rg.normal(size=3);v/=np.linalg.norm(v);A=abs(v@(Mhat+E)@z);Ah=abs(v@Mhat@z);eps=.08*np.linalg.norm(z)
 assert max(0,Ah-eps)-1e-12<=A<=Ah+eps+1e-12
vout=np.array([1.,1.])/np.sqrt(2); M0=np.diag([1.,0]); zout=np.array([1.,0]); assert not np.allclose(M0@vout,vout) and vout@M0@zout!=0
assert .1*gate(0)<.25
assert np.isclose((1.4-.5)/1.6,.5625)
done('Exact feasibility/window, positive off-window gate, item-specific null and map uncertainty bounds')
# Projection communication: independent sender contrast and memory checks.
for _ in range(200):
 Mtest=rg.normal(size=(3,2));ztest=rg.normal(size=2);dtest=rg.normal(size=2);vtest=rg.normal(size=3);vtest/=np.linalg.norm(vtest)
 delta=rg.uniform(-np.pi,np.pi);e=.13
 q=lambda z:float(gate(delta)*(vtest@Mtest@z))
 assert np.isclose(q(ztest+e*dtest)-q(ztest),e*gate(delta)*(vtest@Mtest@dtest),atol=1e-12)
 Av=abs(vtest@Mtest@ztest)
 assert Av*np.exp(-4)-1e-12<=abs(q(ztest))<=Av+1e-12
 assert np.isclose(abs(gate(np.pi)*(vtest@Mtest@ztest)),Av*np.exp(-4))
 kernel=np.array([.2,.3,.5]);signed=rg.uniform(.1,2,3);phases=rg.uniform(-np.pi,np.pi,3)
 assert kernel@(gate(phases)*signed)>=signed.min()*np.exp(-4)-1e-12
assert np.isclose(np.array([.5,.5])@(gate(np.array([0.,0.]))*np.array([1.,-1.])),0.)
done('200 randomized projection communication contrasts, opposite-phase lower bound, same-sign memory extension and cancellation counterexample')
U=np.array([1.,0,0]);V=np.array([0,1.,0]);B=lambda u,v:np.array([0,0,u[0]*v[1]]);A=np.column_stack([U,V]);Q=np.diag([0.,0,1.]);C=B(U,V)[:,None]
assert np.linalg.matrix_rank(np.column_stack([A,C]))-np.linalg.matrix_rank(A)==np.linalg.matrix_rank(Q@C)==1
H,L=1.,.2;chi=.6;f=lambda h,l:h*U+l*V+chi*B(h*U,l*V)
assert np.allclose(Q@(f(H,H)-f(H,L)-f(L,H)+f(L,L)),chi*(H-L)**2*Q@B(U,V))
done('Interaction complement rank and independently evaluated factorial contrast')
r=.6;C=.8;su=.5;sd=.7;fn=lambda r:sensitivity(r,C,su=su,sd=sd)
der=(fn(r+1e-5)-fn(r-1e-5))/2e-5;assert np.isclose(der,C*sd*sd/(r*r*su*su+sd*sd)**1.5)
assert np.isclose(sensitivity(.2,.8,su=1,sd=0),sensitivity(.8,.8,su=1,sd=0))
z=2.;mixed=(1-np.tanh(z)**2)*(1-2*z*np.tanh(z));assert mixed<0
u=.003;assert .018 != .018-u and np.isclose(gamma+O*.018,(gamma+O*u)+O*(.018-u))
done('Sensitivity derivative, pure-upstream and saturation counterexamples, transient onset distinction')
data=json.loads((p/'results.json').read_text());c=data['coverage']
for key,rows,field in [('normal',c['exact_records'],'normal_ci'),('student_t',c['exact_records'],'t_ci'),('noisy',c['noisy_records'],'t_ci'),('bootstrap',c['bootstrap_records'],'ci')]:
 k=sum(row[field][0]<=.6<=row[field][1] for row in rows);assert k==c[key]['k'] and len(rows)==c[key]['n'];assert np.isclose(k/len(rows),c[key]['rate'])
assert data['temporal']['selected_lags']==[2,6];assert data['temporal']['factorial_error']<1e-12
assert data['temporal']['test_mse']['delayed']<data['temporal']['test_mse']['quadratic_excluded']
assert .8<data['joint_recovery']['sd'][2]/data['joint_recovery']['theoretical_tau_sd']<1.2
assert data['mixing']['mixed_rmse']>data['mixing']['clean_rmse']
done('Coverage recomputed from all endpoints, untouched lag selection, delay uncertainty and signal contamination')
# General bilinear complement-rank result, independent of the plotted example.
for _ in range(100):
 n=5;M1=rg.normal(size=(n,2));M2=rg.normal(size=(n,1));AA=np.column_stack([M1,M2]);P=np.linalg.svd(AA,full_matrices=False)[0][:,:3];Q=np.eye(n)-P@P.T
 tensor=rg.normal(size=(n,n,n));Bgen=lambda a,b:np.einsum('ijk,j,k->i',tensor,a,b)
 products=np.column_stack([Bgen(M1[:,a],M2[:,b]) for a in range(2) for b in range(1)])
 inc=np.linalg.matrix_rank(np.column_stack([AA,products]))-np.linalg.matrix_rank(AA)
 assert inc==np.linalg.matrix_rank(Q@products,tol=1e-9)
 assert inc<=min(n-np.linalg.matrix_rank(AA),2)
done('100 randomized interaction span-rank and dimension-bound checks')
# Exact finite-distribution expectation of independent gain-weighted teaching updates.
uvals=[np.array([1.,0.,0.]),np.array([0.,1.,0.]),np.array([1.,1.,0.])]
prob=np.array([.2,.3,.5]);gains=np.array([1.,.4,.7]);G=sum(p*g*np.outer(u,u) for p,g,u in zip(prob,gains,uvals))
step=.3;F=rg.normal(size=(2,3));F0=F.copy();ev=np.linalg.eigvalsh(G);assert step<2/ev.max()
for k in range(1,31):
 F=sum(p*(F-step*g*np.outer(F@u,u)) for p,g,u in zip(prob,gains,uvals))
 assert np.allclose(F,F0@np.linalg.matrix_power(np.eye(3)-step*G,k))
 assert np.allclose(F[:,2],F0[:,2])
assert np.linalg.norm(F[:,:2])<np.linalg.norm(F0[:,:2])
done('Gain-weighted expected learning recursion, excited-subspace contraction and unexcited-direction invariance')
# Explicit regularity counterexample: discontinuous gain can have an unattained infimum.
discontinuous=lambda t: 0. if t==0. else 1.
assert discontinuous(0.)<.5 and all(discontinuous(1./n)>=.5 for n in range(1,101))
assert np.allclose(np.exp(0.*(np.cos(np.linspace(-np.pi,np.pi,100))-1)),1.)
done('First-passage continuity counterexample and zero-concentration gate boundary')
# Worked content-ensemble example: exact enumeration, not a simulation fit.
reader=json.loads((p/'reader_results.json').read_text());T0=np.array([[0.,1.],[1.,0.]]);F0=T0-np.eye(2)
restricted=F0.copy();broad=F0.copy();e1=np.array([1.,0.]);e2=np.array([0.,1.])
for k in range(31):
 assert np.allclose(restricted,np.array(reader['restricted_mean_error'][k]))
 assert np.allclose(broad,np.array(reader['broad_mean_error'][k]))
 assert np.allclose(restricted[:,1],F0[:,1])
 assert np.allclose(np.linalg.norm(restricted,axis=0),reader['restricted_column_error_norm'][k])
 assert np.allclose(np.linalg.norm(broad,axis=0),reader['broad_column_error_norm'][k])
 restricted=sum((restricted-.4*.5*np.outer(restricted@u,u))/2 for u in [e1,-e1])
 broad=sum((broad-.4*.5*np.outer(broad@u,u))/4 for u in [e1,-e1,e2,-e2])
assert np.allclose(np.exp(2*(np.cos(np.pi/2)-1)),np.exp(2*(np.cos(-np.pi/2)-1)))
assert abs(2*1*np.sin(np.pi/2)+1*2*np.sin(-np.pi/2))<1e-12
done('Worked restricted/broad teaching distributions, column-error curves, pathwise unexcited update and multi-band derivative cancellation')
# Independent method-of-steps calculation of reciprocal matrix responses.
rr=json.loads((p/'reciprocal_results.json').read_text())
assert rr['crossing']=={'returns':2,'time_s':.078}
assert rr['direct_only_crossing'] is None and rr['limit_threshold_crossing'] is None
assert np.allclose(rr['first_return_projection'],0.)
assert rr['carrier_difference']<1e-12
for trial in range(100):
 nf,nb=3,2;dt=.001;N=100
 f=rg.normal(size=(3,2));b=rg.normal(size=(2,3))
 f*=.6/np.linalg.norm(f,2);b*=.6/np.linalg.norm(b,2)
 d=rg.normal(size=2);A=f@b
 P=np.zeros((N,3));Q=np.zeros((N,2))
 for j in range(N):
  P[j]=f@Q[j-nf] if j>=nf else 0.
  Q[j]=d+(b@P[j-nb] if j>=nb else 0.)
 for j in range(N):
  expected=np.zeros(3);vec=f@d
  for k in range(max(0,(j-nf)//(nf+nb)+1)):
   expected+=vec;vec=A@vec
  assert np.allclose(P[j],expected,atol=1e-12)
 assert np.allclose((np.eye(3)-A)@np.linalg.solve(np.eye(3)-A,f@d),f@d)
done('100 independent matrix method-of-steps / echo-series checks and stable resolvents')
# Independent positive-channel threshold regimes including zero and limit cases.
from simulate_reciprocal import crossing,step_response,carrier
for aa in [.1,.2,.7]:
 for bb in [0.,.2,.5,.8]:
  limit=aa/(1-bb)
  for theta in [aa/2,aa,(aa+limit)/2,limit,limit*1.1]:
   result_cross=crossing(aa,bb,theta,.018,.012)
   values=aa*np.cumsum(bb**np.arange(1000))
   finite=np.flatnonzero(values>=theta) if theta<limit or theta<=aa else np.array([],dtype=int)
   if result_cross is None:
    assert not len(finite)
   else:
    assert len(finite) and result_cross['returns']==int(finite[0])
    assert abs(result_cross['time_s']-(.018+finite[0]*.03))<1e-12
assert crossing(0.,.5,.2,.018,.012) is None
# Zero direct readout can gain a later contribution through rotation.
f=np.eye(2)*.5;b=np.array([[0.,.5],[.5,0.]])
d=np.array([1.,0.]);v=np.array([0.,1.])
assert v@(f@d)==0 and v@(f@b@f@d)!=0
# Signed feedback cancellation: later readout is not generally monotone.
assert .2+(-.5)*.2 < .2
done('Independent threshold regime checks, equal-limit nonattainment, readout rotation and signed-return counterexamples')
for k in range(100):
 O=2*np.pi*8;pair=[];pair2=[]
 for edge in range(2):
  g,al=rg.normal(size=2);tau=rg.uniform(.01,.03);psi=rg.normal();M=rg.uniform(.1,.5);u=rg.uniform(-.005,.005)
  pair.append(carrier(O,psi,g,al,tau,M))
  pair2.append(carrier(O,psi,g+O*u,al+O*u,tau-u,M))
 assert np.allclose(pair,pair2,atol=1e-12)
 assert np.allclose(pair[0]/(1-pair[0]*pair[1]),pair2[0]/(1-pair2[0]*pair2[1]),atol=1e-12)
done('100 random two-edge carrier ridge checks with resolved onset outside the stationary law')
# General non-invariant readout tails and transient crossing counterexamples.
for _ in range(100):
 A=rg.normal(size=(3,3));A*=.7/np.linalg.norm(A,2)
 p0=rg.normal(size=3);v=rg.normal(size=3);q=np.linalg.norm(A,2)
 limit=v@np.linalg.solve(np.eye(3)-A,p0);partial=np.zeros(3);increment=p0.copy()
 for m in range(40):
  partial+=increment;increment=A@increment
  bound=np.linalg.norm(v)*np.linalg.norm(p0)*q**(m+1)/(1-q)
  assert abs(limit-v@partial)<=bound+1e-12
A=np.array([[0.,.5],[-.5,0.]])
p0=v=np.array([1.,0.]);limit=v@np.linalg.solve(np.eye(2)-A,p0)
assert np.isclose(limit,.8) and v@p0>.9
# Full convolutional loop versus operator Neumann terms.
N=100;source=np.ones(N);hf=np.array([.5,.5]);hb=np.array([1.])
lf=lambda x:.5*shifted(np.convolve(x,hf)[:N],2)
lb=lambda x:.4*shifted(np.convolve(x,hb)[:N],3)
PP=np.zeros(N);QQ=np.zeros(N)
for j in range(N):
 PP[j]=.5*sum(hf[k]*QQ[j-2-k] for k in range(len(hf)) if j>=2+k)
 QQ[j]=1.+(.4*PP[j-3] if j>=3 else 0.)
term=lf(source);series=np.zeros(N)
for k in range(30):series+=term;term=lf(lb(term))
assert np.allclose(PP,series,atol=1e-12)
# Continuous-input approximate identity; its error must vanish with support width.
xx=np.linspace(-1,1,100)
errors=[max(abs(np.mean(np.sin(xx[:,None]-np.linspace(0,eps,200)[None,:]),axis=1)-np.sin(xx))) for eps in [.1,.01,.001]]
assert errors[2]<errors[1]<errors[0]
done('General readout tail certificates, transient overshoot, full convolution loop and instantaneous-processing limit')
# Gaussian noise-whitened interaction innovation and a silent class contrast.
S=np.eye(3)[:,:2];CB=np.array([[0.],[0.],[2.]])
Sigma=np.diag([4.,9.,16.]);W=np.diag([.5,1/3,.25]);Qw=np.diag([0.,0.,1.])
b=CB[:,0];lam=.6*.8*.7;mu=np.array([1.,0.,0.])+lam*b
new_norm=np.linalg.norm(Qw@W@(lam*b))
full=mu@np.linalg.solve(Sigma,mu)
assert np.allclose(full,np.linalg.norm((np.eye(3)-Qw)@W@mu)**2+new_norm**2)
assert np.linalg.matrix_rank(Qw@W@CB)==np.linalg.matrix_rank(np.diag([0.,0.,1.])@CB)==1
assert np.allclose(np.outer(-np.array([1.,0.]),-np.array([0.,1.])),np.outer([1.,0.],[0.,1.]))
done('Interaction-rank to Gaussian discriminability bridge and class-invariant product counterexample')
# Recompute paired Monte Carlo intervals from all individual series outputs.
from scipy.stats import t as student_t
mm=json.loads((p/'mse_comparison_results.json').read_text())
for c in mm['comparisons']:
 delta=np.array([r['test_mse'][c['rival']]-r['test_mse']['delayed'] for r in mm['records']])
 assert np.isclose(delta.mean(),c['mean_difference'])
 expected_ci=delta.mean()+np.array([-1,1])*student_t.ppf(.975,len(delta)-1)*delta.std(ddof=1)/np.sqrt(len(delta))
 assert np.allclose(expected_ci,c['ci95_pointwise'])
 assert c['p_holm']>=c['p_two_sided']
assert mm['n_realizations']==300 and mm['true_lag_selection_count']==300
done('Paired 300-series MSE confidence intervals, selection counts and adjusted-test bounds')
# Independent finite Lyapunov sum and stable non-normal threshold check.
from scipy.linalg import solve_discrete_lyapunov
An=np.array([[.65,1.2],[0,.65]]);pn=np.array([0.,1.]);vn=np.array([1.,0.])
Gn=solve_discrete_lyapunov(An.T,np.eye(2));Gsum=sum(np.linalg.matrix_power(An,k).T@np.linalg.matrix_power(An,k) for k in range(200))
assert np.allclose(Gn,Gsum) and np.allclose(Gn-An.T@Gn@An,np.eye(2))
qn=np.sqrt(1-1/np.linalg.eigvalsh(Gn).max());zn=float(vn@np.linalg.solve(np.eye(2)-An,pn));vals=np.cumsum([vn@np.linalg.matrix_power(An,k)@pn for k in range(100)])
bd=np.sqrt(vn@np.linalg.solve(Gn,vn))*np.sqrt(pn@Gn@pn)*qn**(np.arange(100)+1)/(1-qn)
assert np.all(abs(zn-vals)<=bd+1e-11) and np.flatnonzero(vals>=5)[0]==4
assert max(abs(np.linalg.eigvals(An)))<1 and np.linalg.norm(An,2)>1
assert np.linalg.norm(An@pn)>np.linalg.norm(pn)
done('Stable non-normal Lyapunov identity, independent sum, tail certificates and transient-growth crossing')
result={'status':'PASS','seed':20261005,'checks':checks,'qualification':'Implementation and conditional mathematics only; empirical hypotheses not validated'}
(p/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
