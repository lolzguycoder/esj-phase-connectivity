#!/usr/bin/env python3
"""Paired Monte Carlo model comparison; independent full-series replicates."""
from pathlib import Path
import json
import numpy as np
from scipy.stats import t,ttest_1samp
from model import shifted
ROOT=Path(__file__).resolve().parent
SEED=402600;N_RUNS=300

def replicate(rng):
    n=900;time=np.arange(n)*.005
    z=rng.normal(size=(n,2))
    for j in range(2):
        z[:,j]=np.convolve(z[:,j],np.ones(5)/5,mode='same')
    dj=np.array([[1.,.3],[.2,1.]])
    di=np.array([[.8,-.2],[.1,1.1]])
    translation=di@np.linalg.inv(dj)
    raw=(z@dj.T)@translation.T
    u=.6*shifted(raw[:,0],5)+.4*shifted(raw[:,0],7)
    v=shifted(raw[:,1],4)
    a=(.55+.35*np.sin(2*np.pi*.7*time))*u
    b=(.6+.3*np.cos(2*np.pi*.9*time))*v
    y=.7*a+.4*b+.6*shifted(a,2)*shifted(b,6)+rng.normal(0,.02,n)
    idx=np.arange(30,n);train=idx[:500];valid=idx[500:650];test=idx[650:]
    base=np.column_stack([np.ones(n),a,b]);best=None
    for lf in range(9):
        for lb in range(9):
            x=np.column_stack([base,shifted(a,lf)*shifted(b,lb)])
            coef=np.linalg.lstsq(x[train],y[train],rcond=None)[0]
            risk=np.mean((y[valid]-x[valid]@coef)**2)
            if best is None or risk<best[0]:
                best=(risk,lf,lb,x)
    delayed=best[3]
    features={'additive':base,'instantaneous':np.column_stack([base,a*b]),
              'quadratic_excluded':np.column_stack([base,a*b,a*a,b*b]),
              'delayed':delayed,'quadratic_inclusive':np.column_stack([delayed,a*a,b*b])}
    mse={}
    fit=np.r_[train,valid]
    for name,x in features.items():
        coef=np.linalg.lstsq(x[fit],y[fit],rcond=None)[0]
        mse[name]=float(np.mean((y[test]-x[test]@coef)**2))
    return {'selected_lags':[int(best[1]),int(best[2])],'test_mse':mse}

def run():
    rng=np.random.default_rng(SEED)
    records=[replicate(rng) for _ in range(N_RUNS)]
    names=['additive','instantaneous','quadratic_excluded','quadratic_inclusive']
    comparisons=[]
    for name in names:
        delta=np.array([r['test_mse'][name]-r['test_mse']['delayed'] for r in records])
        mean=delta.mean();sd=delta.std(ddof=1);se=sd/np.sqrt(N_RUNS)
        ci=mean+np.array([-1,1])*t.ppf(.975,N_RUNS-1)*se
        comparisons.append({'rival':name,'mean_difference':float(mean),'sd_difference':float(sd),
                            'ci95_pointwise':ci.tolist(),'p_two_sided':float(ttest_1samp(delta,0).pvalue)})
    order=np.argsort([r['p_two_sided'] for r in comparisons]);running=0.
    for rank,idx in enumerate(order):
        running=max(running,(len(names)-rank)*comparisons[idx]['p_two_sided'])
        comparisons[idx]['p_holm']=min(1.,float(running))
    out={'seed':SEED,'n_realizations':N_RUNS,'units':'squared receiver output units',
         'replication_unit':'independent complete 900-sample series; all models paired within realization',
         'splits':{'train':500,'validation':150,'test':220},
         'lag_grid':list(range(9)),'comparisons':comparisons,'records':records,
         'true_lag_selection_count':sum(r['selected_lags']==[2,6] for r in records),
         'interpretation':'Monte Carlo uncertainty of mean synthetic risk differences, not a neural-data confidence interval; pointwise Student intervals and four-test Holm family'}
    (ROOT/'mse_comparison_results.json').write_text(json.dumps(out,indent=2)+'\n')
    rows=[]
    labels=['Additive','Instantaneous bilinear','Quadratic without delayed product','Quadratic with delayed product']
    for label,row in zip(labels,comparisons):
        lo,hi=np.array(row['ci95_pointwise'])*1000
        pv=row['p_holm'];pf='$<10^{-6}$' if pv<1e-6 else f'{pv:.3g}'
        rows.append(f'{label} & {row["mean_difference"]*1000:.5f} & [{lo:.5f}, {hi:.5f}] & {pf}\\\\')
    tex=r'''\begin{table}[htbp]\centering\small
\caption{Paired test-risk differences over 300 independent synthetic realizations (seed 402600). Positive values favor the delayed bilinear predictor. Differences and confidence limits are in $10^{-3}$ squared output units. Intervals are pointwise 95\%; the four two-sided tests use Holm adjustment.}\label{tab:mse-ci}
\begin{tabularx}{\linewidth}{@{}Yrrr@{}}\toprule
Rival & Mean difference & 95\% interval & Adjusted $p$\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabularx}\end{table}
'''
    (ROOT/'mse_comparison_table.tex').write_text(tex)
    print(json.dumps({'runs':N_RUNS,'true_lag_selection_count':out['true_lag_selection_count'],'comparisons':comparisons},indent=2))

if __name__=='__main__':run()
