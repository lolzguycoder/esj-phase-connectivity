#!/usr/bin/env python3
"""Fixed-gate delayed feedback checks; no fitted biological parameters."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import gate

ROOT = Path(__file__).resolve().parent

def step_response(time, a, beta, forward, backward):
    """Zero prehistory, positive invariant scalar channel, exact event times."""
    time = np.asarray(time)
    loop = forward + backward
    if loop <= 0 or not 0 <= beta < 1:
        raise ValueError('Positive round-trip time and beta in [0,1) required')
    out = np.zeros_like(time, dtype=float)
    for k in range(max(0, int(np.floor((time.max()-forward)/loop))+1)):
        out += a * beta**k * (time >= forward + k*loop)
    return out

def crossing(a, beta, threshold, forward, backward):
    if a <= 0:
        return None
    if threshold <= a:
        return {'returns': 0, 'time_s': forward}
    if beta == 0 or threshold >= a/(1-beta):
        return None
    # Iterate plateaus to avoid logarithmic rounding at exact equality.
    value = a
    k = 0
    while value < threshold:
        k += 1
        value += a*beta**k
    return {'returns': k, 'time_s': forward+k*(forward+backward)}

def carrier(omega, psi, gamma, alpha, delay, translation, kappa=2.):
    return gate(psi-alpha-omega*delay, kappa)*np.exp(-1j*(gamma+omega*delay))*translation

def run():
    forward, backward, a, beta, threshold = .018, .012, .2, .5, .34
    time = np.arange(0, .201, .001)
    recurrent = step_response(time, a, beta, forward, backward)
    one_way = step_response(time, a, 0., forward, backward)
    f = np.diag([.5, 0.]); b = np.diag([0., .5]); d = np.array([1., 0.])
    direct = f @ d; returned = f @ b @ f @ d
    omega = 2*np.pi*8
    pars = [(.25, .8, forward, .55, .9), (-.1, .6, backward, .5, .7)]
    def full_loop(params):
        kf, kb = [carrier(omega, psi, gamma, alpha, delay, m)
                  for gamma, alpha, delay, m, psi in params]
        return kf/(1-kf*kb)
    shifts = [.004, -.002]
    changed = [(g+omega*u, al+omega*u, tau-u, m, psi)
               for (g, al, tau, m, psi), u in zip(pars, shifts)]
    base, compensated = full_loop(pars), full_loop(changed)
    newf, newb = forward-shifts[0], backward-shifts[1]
    result = {'status':'PASS', 'model':'zero-prehistory fixed-gate reciprocal step',
              'units':{'time':'seconds','amplitude':'calibrated arbitrary units'},
              'parameters':{'forward_s':forward,'backward_s':backward,'a':a,'beta':beta,'threshold':threshold},
              'crossing':crossing(a,beta,threshold,forward,backward),
              'direct_only_crossing':crossing(a,0.,threshold,forward,backward),
              'limit_threshold_crossing':crossing(a,beta,.4,forward,backward),
              'direct_projection':direct.tolist(),'first_return_projection':returned.tolist(),
              'carrier_response':[base.real,base.imag],
              'compensated_response':[compensated.real,compensated.imag],
              'carrier_difference':float(abs(base-compensated)),
              'anchored_first_three_times_s':[forward+k*(forward+backward) for k in range(3)],
              'compensated_first_three_times_s':[newf+k*(newf+newb) for k in range(3)],
              'time_s':time.tolist(),'recurrent':recurrent.tolist(),'one_way':one_way.tolist(),
              'qualification':'Constructed examples and implementation checks; no neural fitting or empirical validation'}
    assert result['crossing']['returns']==2 and abs(result['crossing']['time_s']-.078)<1e-12
    assert result['carrier_difference']<1e-12
    fig, axs = plt.subplots(1,3,figsize=(11.5,3.65),layout='constrained')
    axs[0].step(time*1000,recurrent,where='post',label='Reciprocal loop')
    axs[0].step(time*1000,one_way,where='post',label='Reverse path removed',linestyle='--')
    axs[0].axhline(threshold,color='black',linestyle=':',label='Threshold 0.34')
    axs[0].axvline(78,color='gray',linestyle=':',linewidth=1)
    axs[0].set(xlabel='Time (ms)',ylabel='Readout amplitude',title='Completion after two returns',xlim=(0,150),ylim=(0,.43))
    axs[0].legend(fontsize=8,loc='lower right')
    axs[1].bar(['Direct','First return'],[direct[0],returned[0]],color=['#2563a0','#ba5555'])
    axs[1].set(ylabel='Item contribution',title='Nonzero maps; zero return',ylim=(0,.6))
    for row,key in enumerate(['anchored_first_three_times_s','compensated_first_three_times_s']):
        for x in result[key]:
            axs[2].vlines(x*1000,row-.22,row+.22,color=['#2563a0','#ba5555'][row])
    axs[2].set(yticks=[0,1],yticklabels=['Original','Compensated'],xlabel='Onset and return time (ms)',title='Same carrier; different echoes',xlim=(0,100),ylim=(-.6,1.6))
    axs[2].text(3,1.35,'Carrier difference < 1e-12',fontsize=9)
    import io
    buffer=io.BytesIO()
    fig.savefig(buffer,format='pdf')
    (ROOT/'figure_reciprocal.pdf').write_bytes(buffer.getvalue())
    plt.close(fig)
    (ROOT/'reciprocal_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','crossing','carrier_difference','direct_projection','first_return_projection']},indent=2))

if __name__=='__main__':
    run()
