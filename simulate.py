#!/usr/bin/env python3
"""Synthetic checks for the revision. No neural or behavioural data."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
rng = np.random.default_rng(2026)
O = 2 * np.pi * 8


def gate(x, kappa=2.0):
    return np.exp(kappa * (np.cos(x) - 1.0))


def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def panel():
    return plt.subplots(2, 2, figsize=(9.0, 6.4), constrained_layout=True)


def save(fig, n):
    fig.savefig(ROOT / f"figure{n}.pdf")
    plt.close(fig)


out = {}

# Figure 1: gate, orbit, translation, detuning
fig, ax = panel()
d = np.linspace(-np.pi, np.pi, 400)
ax[0, 0].plot(d, gate(d))
ax[0, 0].set(title="A. Arrival gate", xlabel="arrival error (rad)", ylabel="gain")
a = np.linspace(-1, 1, 100)
for eta in [-1, 0, 1]:
    ax[0, 1].plot(a, (eta - a) / O * 1000, label=f"eta={eta}")
ax[0, 1].set(title="B. Equal-offset lines", xlabel="preference (rad)", ylabel="delay (ms)")
ax[0, 1].legend(fontsize=8)
Di = np.array([[1.0, 0.4], [0.2, 1.0]])
z = np.array([1.0, 0.7])
errors = [
    float(np.linalg.norm(r * T @ z - Di @ z))
    for T in [Di, np.eye(2)]
    for r in [1.0, 0.2]
]
ax[1, 0].bar(["exact/open", "exact/low", "wrong/open", "wrong/low"], errors)
ax[1, 0].tick_params(axis="x", labelrotation=20)
ax[1, 0].set(title="C. Translation versus gain", ylabel="target discrepancy")
f = np.linspace(0, 10, 200)
tt = np.linspace(0, 0.1, 1000)
ax[1, 1].plot(f, gate(2 * np.pi * f[:, None] * tt).mean(axis=1))
ax[1, 1].set(title="D. Detuning over 100 ms", xlabel="frequency difference (Hz)", ylabel="mean gate")
save(fig, 1)
out["translation_errors"] = errors

# Figure 2: independent marker channels
fig, ax = panel()
t = np.linspace(0, 45, 451)
true = np.array([12.0, 21.0, 26.0])
grid = np.arange(0, 40.0001, 0.25)
estimates = []


def logistic(time, onset):
    return 1 / (1 + np.exp(-(time - onset)))


for onset, label in zip(true, ["arrival", "ignition-like", "output"]):
    mean = logistic(t, onset)
    obs = mean + rng.normal(0, 0.025, len(t))
    sse = ((obs[None, :] - logistic(t[None, :], grid[:, None])) ** 2).sum(axis=1)
    estimates.append(float(grid[sse.argmin()]))
    ax[0, 0].plot(t, obs, alpha=0.5, label=label)
    ax[0, 0].plot(t, mean, color="black", lw=0.7)
    ax[0, 1].plot(grid, sse, label=label)
ax[0, 0].set(title="A. Independent marker channels", xlabel="time (ms)", ylabel="signal")
ax[0, 0].legend(fontsize=8)
ax[0, 1].set(title="B. Onset SSE", xlabel="candidate onset (ms)", ylabel="SSE")
ax[0, 1].legend(fontsize=8)
intervals = np.diff(np.r_[0, estimates])
x = np.arange(3)
ax[1, 0].bar(x - 0.18, [12, 9, 5], 0.36, label="true")
ax[1, 0].bar(x + 0.18, intervals, 0.36, label="recovered")
ax[1, 0].set(
    xticks=x,
    xticklabels=["conduction", "pre-marker", "post-marker"],
    ylabel="ms",
    title="C. Marker differences",
)
ax[1, 0].legend()
J = np.array([[1, O, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 1, 1.0]])
ax[1, 1].semilogy(np.arange(1, 5), np.linalg.svd(J, compute_uv=False), "o-", label="anchored")
ax[1, 1].plot([1], np.linalg.svd(J[:1], compute_uv=False), "s", label="phase only")
ax[1, 1].set(
    title="D. Observation ranks: 4 vs 1",
    xlabel="singular-value index",
    ylabel="singular value",
)
ax[1, 1].legend()
save(fig, 2)
out["onsets_ms"] = estimates
out["intervals_ms"] = intervals.tolist()

# Figure 3: ordering centroid
fig, ax = panel()
N = 12
slots = np.arange(N) * 0.02
q = np.arange(1, N + 1, dtype=float)
q /= q.sum()
ident = np.arange(N)
mid = ident.copy()
mid[4:8] = mid[4:8][::-1]
perms = [ident, mid, ident[::-1], np.r_[ident[6:], ident[:6]]]
names = ["identity", "middle", "reverse", "half swap"]


def spectrum(w, p):
    return np.sum(q * np.exp(-1j * w * slots[p]))


cent = np.array([np.sum(q * (slots[p] - slots)) for p in perms])
w = 1e-5
slope = np.array([-np.angle(spectrum(w, p) / spectrum(w, ident)) / w for p in perms])
finite = np.array([-np.angle(spectrum(O, p) / spectrum(O, ident)) / O for p in perms])
ax[0, 0].bar(names, cent * 1000)
ax[0, 0].set(title="A. Weighted centroid shift", ylabel="ms")
ax[0, 1].plot(cent * 1000, slope * 1000, "o")
ax[0, 1].plot([-80, 0], [-80, 0], "--")
ax[0, 1].set(title="B. Near-zero spectral slope", xlabel="centroid (ms)", ylabel="slope (ms)")
x = np.arange(4)
ax[1, 0].bar(x - 0.18, cent * 1000, 0.36, label="centroid")
ax[1, 0].bar(x + 0.18, finite * 1000, 0.36, label="8 Hz phase")
ax[1, 0].set(xticks=x, xticklabels=names, ylabel="ms", title="C. Finite-frequency failure")
ax[1, 0].legend(fontsize=8)
freq = np.linspace(0.001, 12, 400)
vals = [
    -np.angle(spectrum(2 * np.pi * f, perms[-1]) / spectrum(2 * np.pi * f, ident))
    / (2 * np.pi * f)
    for f in freq
]
ax[1, 1].plot(freq, np.array(vals) * 1000)
ax[1, 1].axhline(cent[-1] * 1000, ls="--", color="black")
ax[1, 1].set(title="D. Approximation regime", xlabel="frequency (Hz)", ylabel="estimated shift (ms)")
for axx in [ax[0, 0], ax[1, 0]]:
    axx.tick_params(axis="x", labelrotation=15)
save(fig, 3)
out["centroids_ms"] = (cent * 1000).tolist()
out["spectral_slopes_ms"] = (slope * 1000).tolist()
out["finite_phase_ms"] = (finite * 1000).tolist()

# Figure 4: sensitivity, saturation, serial product, imposed access/trace split
fig, ax = panel()
r = np.linspace(0.001, 1, 300)
for su, sd, label in [(0, 1, "downstream"), (0.7, 0.7, "mixed"), (1, 0, "upstream")]:
    ax[0, 0].plot(r, r / np.sqrt(r * r * su * su + sd * sd), label=label)
ax[0, 0].set(title="A. Conditional sensitivity", xlabel="gain", ylabel="d'")
ax[0, 0].legend(fontsize=8)
zv = np.linspace(0, 2, 300)
cross = (1 - np.tanh(zv) ** 2) * (1 - 2 * zv * np.tanh(zv))
ax[0, 1].plot(zv, cross)
ax[0, 1].axhline(0, color="black", lw=0.7)
ax[0, 1].set(title="B. Saturation mixed derivative", xlabel="z = wrC", ylabel="derivative / w")
ax[1, 0].plot(d, gate(d), label="second aligned")
ax[1, 0].plot(d, gate(d) * gate(np.pi / 2), label="second at pi/2")
ax[1, 0].set(title="C. Serial product", xlabel="first-edge error", ylabel="end-to-end gain")
ax[1, 0].legend(fontsize=8)
# Imposed split: access follows the gate; trace updates only if learning opportunity is open.
local = 0.80
access_off = local * float(gate(np.pi))
access_on = local * float(gate(0.0))
m_closed = 0.0
m_open = 0.0
for _ in range(5):
    m_open += 0.1 * (local - m_open)  # Eq. (plastic), u=1, ell=r=1
labels = ["access\noff", "access\non", "trace\nclosed", "trace\nopen"]
vals = [access_off, access_on, m_closed, m_open]
ax[1, 1].bar(labels, vals, color=["#4c78a8", "#4c78a8", "#f58518", "#f58518"])
ax[1, 1].set(title="D. Imposed access/trace split", ylabel="model units")
save(fig, 4)
out["access_trace"] = {
    "local": local,
    "access_off": access_off,
    "access_on": access_on,
    "trace_closed": m_closed,
    "trace_open": m_open,
    "note": "Split is imposed by the generator: access uses the gate; trace updates only if the learning flag is open.",
}

# Figure 5: interaction recovery with uncertainty and a flexible competitor.
fig, ax = panel()
chi, high, low = 0.6, 1.0, float(gate(np.pi / 2))
rp, rc = np.meshgrid(np.linspace(0, 1, 80), np.linspace(0, 1, 80))
im = ax[0, 0].imshow(chi*rp*rc, origin="lower", extent=[0,1,0,1], aspect="auto")
ax[0,0].set(title="A. Stipulated interaction", xlabel="unreported-path gain", ylabel="report-associated gain")
fig.colorbar(im, ax=ax[0,0])
contrast=chi*(high-low)**2
ax[0,1].bar(["coupled","additive","null","sign flip"], [contrast,0,0,-contrast])
ax[0,1].set(title="B. Factorial contrast", ylabel="HH - HL - LH + LL")
records={}
for truth in [0.6,0.0]:
    rec={k:[] for k in ["chi","ci95","additive_mse","mixed_mse","quadratic_mse"]}
    for run in range(60):
        samples=[]
        for n in [500,500]:
            u,v=rng.uniform(-1,1,(2,n))
            r1,r2=gate(rng.uniform(-np.pi,np.pi,(2,n)))
            a,b=r1*u,r2*v
            base=np.column_stack([np.ones(n),a,b])
            full=np.column_stack([base,a*b])
            quad=np.column_stack([full,a*a,b*b])
            y=0.2+0.7*a+0.4*b+truth*a*b+rng.normal(0,0.02,n)
            samples.append((base,full,quad,y))
        tr,te=samples
        for idx,name in enumerate(["additive_mse","mixed_mse","quadratic_mse"]):
            coef=np.linalg.lstsq(tr[idx],tr[3],rcond=None)[0]
            rec[name].append(float(np.mean((te[3]-te[idx]@coef)**2)))
            if idx==1:
                residual=tr[3]-tr[1]@coef
                var=residual@residual/(len(residual)-tr[1].shape[1])
                se=np.sqrt(var*np.linalg.inv(tr[1].T@tr[1])[-1,-1])
                rec["chi"].append(float(coef[-1]))
                rec["ci95"].append([float(coef[-1]-1.96*se),float(coef[-1]+1.96*se)])
    rec["mean_chi"]=float(np.mean(rec["chi"]))
    rec["sd_chi"]=float(np.std(rec["chi"],ddof=1))
    rec["coverage95"]=float(np.mean([lo<=truth<=hi for lo,hi in rec["ci95"]]))
    records[str(truth)]=rec
x=np.arange(2)
for i,(name,label) in enumerate([("additive_mse","additive"),("mixed_mse","bilinear"),("quadratic_mse","quadratic")]):
    ax[1,0].bar(x+(i-1)*0.24,[np.mean(records[k][name]) for k in ["0.6","0.0"]],0.24,label=label)
ax[1,0].set(xticks=x,xticklabels=["coupled truth","additive truth"],title="C. Independent test predictions",ylabel="test MSE")
ax[1,0].legend(fontsize=8)
for k,rec in records.items():
    val=np.array(rec["chi"][:15]); ci=np.array(rec["ci95"][:15])
    ax[1,1].errorbar(np.arange(15),val,yerr=np.vstack([val-ci[:,0],ci[:,1]-val]),fmt="o",label="truth "+k)
ax[1,1].set(title="D. First 15 estimates with 95% intervals",xlabel="realization",ylabel="coupling coefficient")
ax[1,1].legend(fontsize=8)
save(fig,5)
out["mixed_term"]={"factorial_contrast":contrast,"realizations":60,"recovery":records,
    "note":"OLS intervals conditional on exact observed gains/features and independent Gaussian noise; the quadratic comparator contains the bilinear model."}

# Figure 6: matched ablations. A 16-Hz harmonic is removed by the ideal 6-10 Hz filter.
fs,nsamp,f0=250.,500,8.
tt=np.arange(nsamp)/fs

def ar1(rg,n,scale):
    e=rg.normal(size=n); x=np.zeros(n)
    for i in range(1,n): x[i]=0.85*x[i-1]+e[i]
    return x/(np.std(x)+1e-12)*scale

def band_limit(x,lo=6,hi=10):
    spec=np.fft.rfft(x); freqs=np.fft.rfftfreq(len(x),1/fs)
    spec[(freqs<lo)|(freqs>hi)]=0
    return np.fft.irfft(spec,n=len(x))

def analytic_phase(x):
    spec=np.fft.fft(x); h=np.zeros(len(x));h[0]=h[len(x)//2]=1;h[1:len(x)//2]=2
    return np.angle(np.fft.ifft(spec*h))

def observe(delta,mixing,common,harmonic,snr,rg):
    sender=np.cos(2*np.pi*f0*tt); receiver=np.cos(2*np.pi*f0*tt-delta)
    drive=common*np.cos(2*np.pi*f0*tt+0.4)
    a=sender+mixing*receiver+drive+harmonic*np.cos(4*np.pi*f0*tt)
    b=receiver+mixing*sender+drive+harmonic*np.cos(4*np.pi*f0*tt-2*delta)
    scale=np.std(sender)/10**(snr/20)
    a+=ar1(rg,nsamp,scale); b+=ar1(rg,nsamp,scale)
    sl=slice(nsamp//4,3*nsamp//4)
    dp=analytic_phase(band_limit(a))[sl]-analytic_phase(band_limit(b))[sl]
    return float(np.angle(np.mean(np.exp(1j*dp))))

alphas=np.linspace(-np.pi,np.pi,49); kappagrid=np.linspace(.25,8,32)
aa,kk=np.meshgrid(alphas,kappagrid,indexing="ij")
def fit_gate(obs,y):
    templates=gate(obs[None,:]-aa.ravel()[:,None],kk.ravel()[:,None])
    gains=np.maximum(0,templates@y/(np.sum(templates**2,axis=1)+1e-12))
    residual=y[None,:]-gains[:,None]*templates
    idx=np.argmin(np.sum(residual**2,axis=1))
    return float(aa.ravel()[idx]),float(kk.ravel()[idx]),float(gains[idx])
def fourier(x):
    return np.column_stack([np.ones(len(x))]+[f(k*x) for k in range(1,7) for f in [np.sin,np.cos]])
conditions=[("clean10",0,0,0,10),("clean0",0,0,0,0),("mix",.2,0,0,0),
    ("drive",0,.35,0,0),("harm",0,0,.2,0),("mix+drive",.2,.35,0,0),("all",.2,.35,.2,0)]
summary=[]
phasebox=[]; kappabox=[]; same_harm=[]
for name,mix,drive,harm,snr in conditions:
    rmse=[]; concentration=[]; offsets=[]; testmse=[]; constmse=[]; fmse=[]; saved=[]
    for run in range(24):
        rg=np.random.default_rng(9200+run) # identical inputs/noise across ablations
        delta=rg.uniform(-np.pi,np.pi,160)
        obs=np.array([observe(v,mix,drive,harm,snr,rg) for v in delta])
        y=gate(delta)+rg.normal(0,.15,160)
        tr=slice(0,80);te=slice(80,160)
        alpha,kap,gain=fit_gate(obs[tr],y[tr])
        testmse.append(float(np.mean((y[te]-gain*gate(obs[te]-alpha,kap))**2)))
        constmse.append(float(np.mean((y[te]-np.mean(y[tr]))**2)))
        coef=np.linalg.lstsq(fourier(obs[tr]),y[tr],rcond=None)[0]
        fmse.append(float(np.mean((y[te]-fourier(obs[te])@coef)**2)))
        rmse.append(float(np.sqrt(np.mean(wrap(obs-delta)**2))))
        offsets.append(abs(float(wrap(alpha))));concentration.append(kap);saved.append(obs)
    summary.append({"condition":name,"phase_rmse":float(np.mean(rmse)),"mean_kappa":float(np.mean(concentration)),
        "sd_kappa":float(np.std(concentration,ddof=1)),"offset_mae":float(np.mean(offsets)),
        "gate_test_mse":float(np.mean(testmse)),"constant_test_mse":float(np.mean(constmse)),
        "fourier_test_mse":float(np.mean(fmse)),"gate_test_wins_constant":int(np.sum(np.array(testmse)<constmse))})
    phasebox.append(rmse);kappabox.append(concentration)
    if name=="clean0": baseline=np.array(saved)
    if name=="harm": same_harm.append(float(np.max(abs(wrap(np.array(saved)-baseline)))))
    if name=="mix+drive": mixedbaseline=np.array(saved)
    if name=="all": same_harm.append(float(np.max(abs(wrap(np.array(saved)-mixedbaseline)))))
false=[]
for run in range(24):
    rg=np.random.default_rng(19300+run);delta=rg.uniform(-np.pi,np.pi,160)
    obs=np.array([observe(v,.2,.35,.2,0,rg) for v in delta])
    y=.55+.35*np.cos(2*delta)+rg.normal(0,.15,160)
    alpha,kap,gain=fit_gate(obs[:80],y[:80])
    gm=float(np.mean((y[80:]-gain*gate(obs[80:]-alpha,kap))**2))
    cm=float(np.mean((y[80:]-np.mean(y[:80]))**2))
    coef=np.linalg.lstsq(fourier(obs[:80]),y[:80],rcond=None)[0]
    fm=float(np.mean((y[80:]-fourier(obs[80:])@coef)**2))
    false.append([gm,cm,fm])
false=np.array(false)
fig,ax=panel();names=[c[0] for c in conditions]
ax[0,0].boxplot(phasebox,tick_labels=names);ax[0,0].set(title="A. Matched observation ablations",ylabel="phase RMSE (rad)")
ax[0,1].boxplot(kappabox,tick_labels=names);ax[0,1].axhline(2,ls="--",color="black");ax[0,1].set(title="B. Practical recovery",ylabel="concentration (truth 2)")
for a in ax[0]: a.tick_params(axis="x",labelrotation=35)
x=np.arange(len(names))
for i,(key,label) in enumerate([("gate_test_mse","gate"),("constant_test_mse","constant"),("fourier_test_mse","Fourier")]):
    ax[1,0].plot(x,[s[key] for s in summary],"o-",label=label)
ax[1,0].set(xticks=x,xticklabels=names,title="C. Held-out prediction",ylabel="MSE");ax[1,0].tick_params(axis="x",labelrotation=35);ax[1,0].legend(fontsize=8)
ax[1,1].bar(["gate","constant","Fourier"],false.mean(axis=0));ax[1,1].set(title="D. Two-cycle alternative generator",ylabel="held-out MSE")
save(fig,6)
out["source_mixing"]={"summary":summary,"realizations":24,"harmonic_ablation_max_phase_difference":same_harm,
    "alternative_generator_mse":false.mean(axis=0).tolist(),"false_gate_wins_constant":int(np.sum(false[:,0]<false[:,1])),
    "false_gate_wins_fourier":int(np.sum(false[:,0]<false[:,2])),
    "note":"Exact 8/16-Hz cosines over 2 seconds; 6-10 Hz ideal FFT filter removes the second harmonic. Source mixing and common drive cause the observed distortion. Test trials never used in fits."}

# Figure 7: delayed dictionary translation and finite-memory cross-path interaction.
# Signals in receiver coordinates after specified translation and conduction delays.
rg=np.random.default_rng(4026)
length=900;times=np.arange(length)*.005
z=rg.normal(size=(length,2))
# Smooth broadband content with zero padding; known finite processing kernels.
for j in range(2): z[:,j]=np.convolve(z[:,j],np.ones(5)/5,mode="same")
Dj=np.array([[1.,.3],[.2,1.]])
Di=np.array([[.8,-.2],[.1,1.1]])
T=Di@np.linalg.inv(Dj)
raw=(z@Dj.T)@T.T
assert np.allclose(raw,z@Di.T)
def delayed(x,d):
    y=np.zeros_like(x)
    if d==0:return x.copy()
    y[d:]=x[:-d]
    return y
# Total delays: 3 conduction + 2/4 processing samples; weights .6/.4.
U=.6*delayed(raw[:,0],5)+.4*delayed(raw[:,0],7)
V=delayed(raw[:,1],4)
rp=.55+.35*np.sin(2*np.pi*.7*times);rc=.6+.3*np.cos(2*np.pi*.9*times)
a=rp*U;b=rc*V
# additional interaction memory, 2 and 6 samples, is distinct from conduction
c=delayed(a,2)*delayed(b,6)
y=.7*a+.4*b+.6*c+rg.normal(0,.02,length)
idx=np.arange(30,length);train=idx[:500];valid=idx[500:650];test=idx[650:]
base=np.column_stack([np.ones(length),a,b])
selected=None
for lp in range(9):
    for lc in range(9):
        design=np.column_stack([base,delayed(a,lp)*delayed(b,lc)])
        coef=np.linalg.lstsq(design[train],y[train],rcond=None)[0]
        mse=float(np.mean((y[valid]-design[valid]@coef)**2))
        if selected is None or mse<selected[0]: selected=(mse,lp,lc,design)
_,lp,lc,design=selected
fits={"additive":base,"instantaneous":np.column_stack([base,a*b]),"delayed":design,
      "quadratic":np.column_stack([design,a*a,b*b])}
mses={};preds={}
for label,X in fits.items():
    coef=np.linalg.lstsq(X[np.r_[train,valid]],y[np.r_[train,valid]],rcond=None)[0]
    preds[label]=X@coef
    mses[label]=float(np.mean((y[test]-preds[label][test])**2))
# Gate factorial contrast at frozen features, including delayed interaction.
H,L=1.,.2
F=lambda p,c: .7*p*U+.4*c*V+.6*delayed(p*U,2)*delayed(c*V,6)
contrast_series=F(H,H)-F(H,L)-F(L,H)+F(L,L)
expected=.6*(H-L)**2*delayed(U,2)*delayed(V,6)
fig,ax=panel()
window=slice(0,120)
ax[0,0].plot(times[window],raw[window,0],label="translated content")
ax[0,0].plot(times[window],U[window],label="delayed + processed")
ax[0,0].set(title="A. Dictionary transfer and processing",xlabel="time (s)",ylabel="content units");ax[0,0].legend(fontsize=8)
ax[0,1].plot(times[window],contrast_series[window],label="factorial contrast")
ax[0,1].plot(times[window],expected[window],"--",label="derived prediction")
ax[0,1].set(title="B. Finite-memory interaction",xlabel="time (s)",ylabel="contrast");ax[0,1].legend(fontsize=8)
ax[1,0].bar(list(mses),list(mses.values()));ax[1,0].tick_params(axis="x",labelrotation=20)
ax[1,0].set(title="C. Untouched temporal test segment",ylabel="MSE")
ax[1,1].plot(times[test],y[test],label="synthetic outcome",alpha=.65)
ax[1,1].plot(times[test],preds["delayed"][test],label="delayed fit")
ax[1,1].set(title="D. Test prediction",xlabel="time (s)",ylabel="content units");ax[1,1].legend(fontsize=8)
save(fig,7)
out["delayed_dictionary"]={"sample_ms":5,"conduction_samples":3,"processing_samples":[2,4],"processing_weights":[.6,.4],
    "interaction_lags_true":[2,6],"selected_lags":[lp,lc],"test_mse":mses,
    "factorial_max_error":float(np.max(abs(contrast_series-expected))),
    "note":"Known conduction, encoding maps, processing kernel, and exact features. Selected interaction lags on validation only. This does not identify separate biological conduction/processing latencies."}
(ROOT/"results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"interaction":{k:{x:v[x] for x in ["mean_chi","sd_chi","coverage95"]} for k,v in records.items()},
    "mixing":out["source_mixing"],"delayed":out["delayed_dictionary"]},indent=2))
