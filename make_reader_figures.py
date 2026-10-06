#!/usr/bin/env python3
"""Vector roadmap and exact mean-learning example; no empirical data."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
P=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(8,5.2));ax.set(xlim=(0,10.7),ylim=(0,7.5));ax.axis('off')
def box(x,y,title,desc,color):
 patch=FancyBboxPatch((x,y),3.8,1.15,boxstyle='round,pad=0.12',fc=color,ec='#35556b',lw=1.2);ax.add_patch(patch)
 ax.text(x+1.9,y+.83,title,ha='center',va='center',fontsize=11,fontweight='bold')
 ax.text(x+1.9,y+.35,desc,ha='center',va='center',fontsize=10.5)
def arrow(a,b,style='solid',color='#35556b'):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=12,lw=1.2,linestyle=style,color=color,connectionstyle='arc3'))
ax.text(2.2,7.1,'Measurement: what can be identified?',ha='center',fontsize=11,color='#35556b')
ax.text(7.7,7.1,'Content: what can be delivered?',ha='center',fontsize=11,color='#35556b')
box(.3,5.4,'1. Observation model',r'Offsets $\xi$ and $\eta$'+'\nPhase and gain calibration','#e8f1f8')
box(.3,3.0,'2. Identifiability ridge','One-band ambiguity\nTwo bands + gain scan','#e8f1f8')
box(5.8,5.4,'3. Projection and support',r'Map $M$; receiver readout $v$'+'\nNonzero projection delivers','#eaf3e9')
box(5.8,3.0,'4. Threshold crossing','Amplitude clears threshold\nCrossing may never occur','#eaf3e9')
box(5.8,.6,'5. Translation learning','Excited errors can decrease\nUnexcited errors stay fixed','#fff1df')
arrow((2.2,5.25),(2.2,4.32));ax.text(2.2,4.8,'same observation law',ha='center',fontsize=8.5)
arrow((7.7,5.25),(7.7,4.32));ax.text(7.7,4.8,'item amplitude + phase gate',ha='center',fontsize=8.5)
arrow((4.25,3.58),(5.64,3.58),'dashed');ax.text(4.95,4.2,'calibrated\ngate offset',ha='center',fontsize=8.5)
# Feedback to support uses an outer path; it is not a derivation of learning from completion.
ax.plot([9.72,10.2,10.2],[1.17,1.17,5.97],color='#35556b',ls='--',lw=1.2)
arrow((10.2,5.97),(9.72,5.97),'dashed')
ax.text(10.4,3.58,'updated map',rotation=90,ha='center',va='center',fontsize=8.5)
box(.3,.6,'Reciprocal return test','Map products and echoes\nRound-trip waiting time','#f0eaf7')
arrow((2.2,1.88),(2.2,2.86),'dashed')
ax.text(2.9,2.35,'echo timing',ha='left',fontsize=8.5)
arrow((5.65,3.0),(4.22,1.65),'dashed')
fig.savefig(P/'figure_roadmap.pdf',bbox_inches='tight');plt.close(fig)
n=np.arange(31);T0=np.array([[0.,1.],[1.,0.]]);target=np.eye(2);F0=T0-target
restricted=np.array([F0@np.diag([.8**k,1.]) for k in n]);broad=np.array([.9**k*F0 for k in n])
re=np.linalg.norm(restricted,axis=1);be=np.linalg.norm(broad,axis=1)
fig,axes=plt.subplots(1,2,figsize=(8,3.1),constrained_layout=True,sharey=True)
for ax,curves,title in zip(axes,[re,be],['Restricted teaching: only coordinate 1','Broader teaching: both coordinates']):
 ax.plot(n,curves[:,0],label='Coordinate 1',color='#277da1');ax.plot(n,curves[:,1],label='Coordinate 2',color='#d1495b',ls='--');ax.set(xlabel='Teaching iteration',title=title,ylim=(0,1.55));ax.spines[['top','right']].set_visible(False);ax.legend(fontsize=8)
axes[0].set_ylabel('Norm of mean column error')
fig.savefig(P/'figure_learning_example.pdf');plt.close(fig)
(P/'reader_results.json').write_text(json.dumps({'scope':'exact conditional teaching-model calculation','steps':n.tolist(),'gain':.5,'step_size':.4,'restricted_G':[[.5,0],[0,0]],'broad_G':[[.25,0],[0,.25]],'restricted_mean_error':restricted.tolist(),'broad_mean_error':broad.tolist(),'restricted_column_error_norm':re.tolist(),'broad_column_error_norm':be.tolist()},indent=2)+'\n')
print('Roadmap and exact learning example generated.')
