#!/usr/bin/env python3
"""Every revised result is computed here from independent fixed seeds. Synthetic only."""
from pathlib import Path
import json,platform
import numpy as np
import scipy
from scipy.stats import t,binom
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import gate,wrap,complex_mean,gate_window,sensitivity,ols,shifted
ROOT=Path(__file__).resolve().parent
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
def save(f,n):f.savefig(ROOT/(n+'.pdf'));plt.close(f)
def wilson(k,n):
 p=k/n;z=1.95996398454;d=1+z*z/n;c=(p+z*z/(2*n))/d;r=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
 return [float(c-r),float(c+r)]
def bootstrap(X,y,rg,B=2000):
 XX=np.einsum('ni,nj->nij',X,X).reshape(len(X),-1);XY=X*y[:,None];vals=[]
 for i in range(0,B,100):
  w=rg.multinomial(len(X),np.ones(len(X))/len(X),size=min(100,B-i));lhs=(w@XX).reshape(-1,4,4);rhs=w@XY
  vals.extend(np.linalg.solve(lhs,rhs[...,None])[:,-1,0].tolist())
 return np.quantile(vals,[.025,.975]).tolist()
def run():
 out={'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__},'scope':'synthetic conditional model verification'}
 rg=np.random.default_rng(8102026);om=2*np.pi*np.array([8.,16.]);O=om[0];gamma,alpha,tau=.35,.8,.018;truth=np.array([gamma,alpha,tau]);est=[];psi=np.linspace(-np.pi,np.pi,48,endpoint=False)
 for _ in range(300):
  ph=gamma+om[:,None]*tau+rg.normal(0,.2,(2,32));gg,tt=np.linalg.solve(np.column_stack([np.ones(2),om]),ph.mean(axis=1))
  y=.9*gate(psi-alpha-O*tau)+rg.normal(0,.02,48);start=psi[y.argmax()]
  fit=least_squares(lambda z:z[0]*gate(psi-z[1])-y,[.9,start],bounds=([0,start-np.pi],[2,start+np.pi]));bb=float(wrap(fit.x[1]-O*tt));est.append([gg,bb,tt])
 est=np.array(est);out['joint_recovery']={'seed':8102026,'runs':300,'phase_trials_per_frequency':32,'phase_noise_sd':.2,'gate_points':48,'gate_noise_sd':.02,'truth':truth.tolist(),'mean':est.mean(axis=0).tolist(),'sd':est.std(axis=0,ddof=1).tolist(),'estimates':est.tolist(),'theoretical_tau_sd':float(np.sqrt(2)*.2/np.sqrt(32)/(om[1]-om[0]))}
 fig,ax=plt.subplots(1,3,figsize=(10,3),constrained_layout=True)
 for j,(name,scale) in enumerate([(r'Transfer phase $\gamma$ (rad)',1),(r'Receptive center $\alpha$ (rad)',1),(r'Delay $\tau$ (ms)',1000)]):
  ax[j].hist(est[:,j]*scale,bins=20,color='#277da1');ax[j].axvline(truth[j]*scale,color='#d1495b',ls='--');ax[j].set(xlabel=name,ylabel='Runs' if j==0 else '')
 save(fig,'figure_joint')
 S=complex_mean(.3,O,gamma,alpha,tau);err=max(abs(complex_mean(.3,O,gamma+O*u,alpha+O*u,tau-u)-S) for u in np.linspace(-.015,.018,100));out['ridge']={'max_joint_mean_error':float(err)}
 Ahat=.5;e=.08;th=.25;d=np.linspace(-np.pi,np.pi,501)
 out['delivery']={'Ahat':Ahat,'error_bound':e,'threshold':th,'robust_window':gate_window(Ahat-e,th),'possible_window':gate_window(Ahat+e,th),'gate_pi':float(gate(np.pi)),'hitting_time':(1.4-.5)/1.6}
 out['interaction_geometry']={'additive_rank':2,'augmented_rank':3,'new_direction_dimension':1,'factorial_at_unit_features':.6*(1-.2)**2}
 fig,ax=plt.subplots(1,3,figsize=(10,3),constrained_layout=True)
 ax[0].plot(d,(Ahat-e)*gate(d),label='Lower bound');ax[0].plot(d,(Ahat+e)*gate(d),label='Upper bound');ax[0].axhline(th,color='black',ls='--');ax[0].set(xlabel='Arrival error (rad)',ylabel='Delivered amplitude');ax[0].legend(fontsize=7)
 rr=np.linspace(.02,1,100);ax[1].plot(rr,sensitivity(rr,1,su=1,sd=0),label='Upstream noise');ax[1].plot(rr,sensitivity(rr,1),label='Mixed noise');ax[1].set(xlabel='Gain',ylabel="Sensitivity d'");ax[1].legend(fontsize=7)
 vals=np.linspace(-1,1,21);ax[2].plot(vals,.6*vals,label='Second feature = 1');ax[2].plot(vals,np.zeros_like(vals),'--',label='Additive only');ax[2].set(xlabel='First feature',ylabel='Complement coordinate');ax[2].legend(fontsize=7);save(fig,'figure_delivery')
 rg=np.random.default_rng(9102026);brg=np.random.default_rng(9102027);rec=[];noisy=[];boots=[]
 for run in range(2000):
  u,v=rg.uniform(-1,1,(2,500));r1,r2=gate(rg.uniform(-np.pi,np.pi,(2,500)));a,b=r1*u,r2*v;X=np.column_stack([np.ones(500),a,b,a*b]);y=X@np.array([.2,.7,.4,.6])+rg.normal(0,.02,500)
  c,cov=ols(X,y);se=np.sqrt(cov[-1,-1]);q=t.ppf(.975,496)
  rec.append({'chi':float(c[-1]),'se':float(se),'normal_ci':(c[-1]+np.array([-1,1])*1.96*se).tolist(),'t_ci':(c[-1]+np.array([-1,1])*q*se).tolist()})
  aa=a+rg.normal(0,.15,500);bb=b+rg.normal(0,.15,500);XX=np.column_stack([np.ones(500),aa,bb,aa*bb]);cc,vv=ols(XX,y);ss=np.sqrt(vv[-1,-1]);noisy.append({'chi':float(cc[-1]),'t_ci':(cc[-1]+np.array([-1,1])*q*ss).tolist()})
  if run<60:boots.append({'run':run,'ci':bootstrap(X,y,brg)})
  if run in [59,999,1999]:print('Coverage runs complete:',run+1,flush=True)
 def coverage(rows,key):
  k=sum(r[key][0]<=.6<=r[key][1] for r in rows);return {'k':k,'n':len(rows),'rate':k/len(rows),'wilson':wilson(k,len(rows))}
 out['coverage']={'seed':9102026,'bootstrap_seed':9102027,'n_trials':500,'feature_noise_sd':.15,'exact_records':rec,'noisy_records':noisy,'bootstrap_records':boots,'bootstrap_resamples':2000,'normal':coverage(rec,'normal_ci'),'student_t':coverage(rec,'t_ci'),'noisy':coverage(noisy,'t_ci'),'bootstrap':coverage(boots,'ci'),'first60_t':coverage(rec[:60],'t_ci'),'first60_normal':coverage(rec[:60],'normal_ci'),'mean_chi':float(np.mean([z['chi'] for z in rec])),'sd_chi':float(np.std([z['chi'] for z in rec],ddof=1)),'noisy_mean_chi':float(np.mean([z['chi'] for z in noisy])),'old_52_60_tail':float(binom.cdf(52,60,.95))}
 fig,ax=plt.subplots(1,2,figsize=(8,3),constrained_layout=True);names=['Normal','Student t','Noisy features','Bootstrap'];summ=[out['coverage'][k] for k in ['normal','student_t','noisy','bootstrap']];yy=np.array([s['rate'] for s in summ]);ci=np.array([s['wilson'] for s in summ])
 ax[0].errorbar(np.arange(4),yy,yerr=np.maximum(0,np.stack([yy-ci[:,0],ci[:,1]-yy])),fmt='o',capsize=4);ax[0].axhline(.95,color='black',ls='--');ax[0].set(xticks=np.arange(4),xticklabels=names,ylim=(-.03,1.03),ylabel='Coverage');ax[0].tick_params(axis='x',labelrotation=15)
 ax[1].hist([z['chi'] for z in rec],bins=35,alpha=.65,label='Exact');ax[1].hist([z['chi'] for z in noisy],bins=35,alpha=.65,label='Noisy');ax[1].axvline(.6,color='black',ls='--');ax[1].set(xlabel='Coupling estimate');ax[1].legend(fontsize=8);save(fig,'figure_coverage')
 rg=np.random.default_rng(4026);n=900;tt=np.arange(n)*.005;z=rg.normal(size=(n,2))
 for j in range(2):z[:,j]=np.convolve(z[:,j],np.ones(5)/5,mode='same')
 Dj=np.array([[1,.3],[.2,1.]]);Di=np.array([[.8,-.2],[.1,1.1]]);T=Di@np.linalg.inv(Dj);raw=(z@Dj.T)@T.T;U=.6*shifted(raw[:,0],5)+.4*shifted(raw[:,0],7);V=shifted(raw[:,1],4);a=(.55+.35*np.sin(2*np.pi*.7*tt))*U;b=(.6+.3*np.cos(2*np.pi*.9*tt))*V;y=.7*a+.4*b+.6*shifted(a,2)*shifted(b,6)+rg.normal(0,.02,n)
 idx=np.arange(30,n);train=idx[:500];valid=idx[500:650];test=idx[650:];base=np.column_stack([np.ones(n),a,b]);best=None
 for lp in range(9):
  for lc in range(9):
   X=np.column_stack([base,shifted(a,lp)*shifted(b,lc)]);c=np.linalg.lstsq(X[train],y[train],rcond=None)[0];m=np.mean((y[valid]-X[valid]@c)**2)
   if best is None or m<best[0]:best=(m,lp,lc,X)
 delayed=best[3];fits={'additive':base,'instantaneous':np.column_stack([base,a*b]),'quadratic_excluded':np.column_stack([base,a*b,a*a,b*b]),'delayed':delayed,'quadratic_inclusive':np.column_stack([delayed,a*a,b*b])};mses={};pred={}
 for name,X in fits.items():
  c=np.linalg.lstsq(X[np.r_[train,valid]],y[np.r_[train,valid]],rcond=None)[0];pred[name]=X@c;mses[name]=float(np.mean((y[test]-pred[name][test])**2))
 F=lambda h,l:.7*h*U+.4*l*V+.6*shifted(h*U,2)*shifted(l*V,6);contrast=F(1,1)-F(1,.2)-F(.2,1)+F(.2,.2);expected=.6*.8**2*shifted(U,2)*shifted(V,6)
 out['temporal']={'seed':4026,'selected_lags':list(best[1:3]),'true_lags':[2,6],'sample_ms':5,'splits':[500,150,220],'test_mse':mses,'factorial_error':float(np.max(abs(contrast-expected)))}
 fig,ax=plt.subplots(1,2,figsize=(9,3),constrained_layout=True);ax[0].bar(np.arange(5),list(mses.values()));ax[0].set(xticks=np.arange(5),xticklabels=['Additive','Instant','Quad excl.','Delayed','Quad incl.'],ylabel='Test MSE');ax[0].tick_params(axis='x',labelrotation=25);ax[1].plot(tt[test],y[test],label='Outcome',alpha=.6);ax[1].plot(tt[test],pred['delayed'][test],label='Delayed fit');ax[1].set(xlabel='Time (s)',ylabel='Output');ax[1].legend(fontsize=8);save(fig,'figure_temporal')
 rg=np.random.default_rng(10102026);tt=np.linspace(0,1,128);ce=[]
 for _ in range(300):
  yy=gamma+(O+40*tt)*tau-.5*40*tau*tau+rg.normal(0,.2,len(tt));slope=np.sum((tt-tt.mean())*(yy-yy.mean()))/np.sum((tt-tt.mean())**2);ce.append(float(slope/40))
 out['chirp']={'seed':10102026,'runs':300,'samples':128,'acceleration':40,'noise_sd':.2,'mean':float(np.mean(ce)),'sd':float(np.std(ce,ddof=1)),'estimates':ce}
 rg=np.random.default_rng(11102026);noise=rg.normal(0,.02,(2,2000))+1j*rg.normal(0,.02,(2,2000));x=np.ones(2000,dtype=complex)+noise[0];y=np.exp(-1j*(gamma+O*tau))*np.ones(2000)+noise[1];common=np.exp(1j*.7);clean=np.angle(y*np.conj(x));mixed=np.angle((y+.7*common)*np.conj(x+.3*common));target=-(gamma+O*tau)
 out['mixing']={'seed':11102026,'samples':2000,'clean_rmse':float(np.sqrt(np.mean(wrap(clean-target)**2))),'mixed_rmse':float(np.sqrt(np.mean(wrap(mixed-target)**2)))}
 fig,ax=plt.subplots(1,2,figsize=(8,3),constrained_layout=True);ax[0].hist(np.array(ce)*1000,bins=20);ax[0].axvline(tau*1000,color='black',ls='--');ax[0].set(xlabel='Chirp delay estimate (ms)',ylabel='Runs');ax[1].hist(clean,bins=30,alpha=.65,label='Clean');ax[1].hist(mixed,bins=30,alpha=.65,label='Common component');ax[1].set(xlabel='Cross phase (rad)');ax[1].legend(fontsize=8);save(fig,'figure_escape_mixing')
 (ROOT/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['delivery','temporal','mixing']},indent=2),flush=True)
if __name__=='__main__':run()
