"""Regenerate manuscript figures from results.
Usage: python3 make_figures.py    (run from code/, writes ../figures/)
Figures 4-6 are modeling-diagnostic plots; values are produced by the
analysis scripts in this directory (t3_strengthen.py, t3_quant_ablation.py)
and the reduced-order tests documented in the manuscript. Numbers below are
the verified outputs of those scripts (see README 'Key numbers')."""
import json, os, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT=os.path.join(os.path.dirname(__file__),'..','figures')
RES=os.path.join(os.path.dirname(__file__),'..','results','t3_confirmatory_results.json')

# ---- Fig 4: lumped vs decomposed regression (from t3_strengthen.py frame-level) ----
def fig4():
    fig,ax=plt.subplots(1,2,figsize=(11,4))
    ax[0].bar(['total\n(lumped)','minority\n(decomposed)'],[0.546,0.820],color=['#c0504d','#4e9a4e'],width=0.5)
    ax[0].set_ylabel('regression R2'); ax[0].set_ylim(0,1)
    ax[0].set_title('Lumped command regression mixes channels;\ndecomposition is cleaner')
    for i,v in enumerate([0.546,0.820]): ax[0].text(i,v+0.02,f'{v:.2f}',ha='center')
    ax[1].bar(['honest','T3 minority'],[-0.022,0.283],color=['#999999','#4e9a4e'],width=0.5)
    ax[1].axhline(0,color='k',lw=0.8); ax[1].set_ylabel('velocity-damping coef. k')
    ax[1].set_title('Damping term is minority-specific\n(absent in honest command)')
    for i,v in enumerate([-0.022,0.283]): ax[1].text(i,v+0.01 if v>0 else v-0.03,f'{v:+.3f}',ha='center')
    plt.suptitle('Channel decomposition reveals a minority-specific velocity-damping term',fontsize=10.5)
    plt.tight_layout(); plt.savefig(os.path.join(OUT,'Figure_4.png'),dpi=300,bbox_inches='tight'); plt.close()

# ---- Fig 5: saturated reduced model vs engine honest latency curve ----
def fig5():
    d=json.load(open(RES))
    eng={r['ctrl_delay_f']:r['honest'] for r in d['E1'] if r['traj']=='circle' and r['tr']==0.30}
    DEL=sorted(eng); engv=[eng[k] for k in DEL]
    sat=[0.292,0.353,0.476,0.691,1.174,2.027,2.200,3.143]
    lin=[0.108,0.129,0.170,0.779,np.nan,np.nan,np.nan,np.nan]
    fig,ax=plt.subplots(figsize=(7,4.3))
    ax.plot(DEL,engv,'ko-',label='engine (honest)',ms=6,lw=2)
    ax.plot(DEL,sat,'g^--',label='reduced + saturation (r~0.96)',ms=6)
    ax.plot(DEL,lin,'rx:',label='reduced, linear (no saturation)',ms=8)
    ax.annotate('linear model diverges\n(engine saturates -> bounded)',xy=(34,3.0),xytext=(8,3.3),
                fontsize=9,color='red',arrowprops=dict(arrowstyle='->',color='red'))
    ax.set_xlabel('control delay (frames)'); ax.set_ylabel('cross-track RMSE'); ax.set_ylim(0,4)
    ax.legend(fontsize=9); ax.grid(alpha=.3)
    ax.set_title('Fixed-speed saturation explains bounded high-delay degradation',fontsize=10)
    plt.tight_layout(); plt.savefig(os.path.join(OUT,'Figure_6.png'),dpi=300,bbox_inches='tight'); plt.close()

# ---- Fig 6: gap prediction failure / scope boundary ----
def fig6():
    d=json.load(open(RES)); DEL=sorted({r['ctrl_delay_f'] for r in d['E1'] if r['traj']=='circle'})
    engGap=[-0.027,0.004,0.045,0.141,0.327,-0.184,-0.006,0.562]
    predGap=[-0.064,-0.066,-0.070,-0.033,0.372,1.025,1.655,0.928]
    fig,ax=plt.subplots(figsize=(7.5,4.3)); x=np.arange(len(DEL)); w=0.38
    ax.bar(x-w/2,engGap,w,label='engine gap (honest-T3)',color='#333333')
    ax.bar(x+w/2,predGap,w,label='reduced-model prediction',color='#c0504d',alpha=0.8)
    ax.axhline(0,color='k',lw=0.8); ax.set_xticks(x); ax.set_xticklabels(DEL)
    ax.set_xlabel('control delay (frames)'); ax.set_ylabel('RMSE gap (>0 = T3 helps)')
    for i in [5,6]: ax.annotate('sign\nmismatch',xy=(i,predGap[i]),xytext=(i-0.3,predGap[i]+0.3),fontsize=8,color='red')
    ax.legend(fontsize=9); ax.grid(alpha=.3,axis='y')
    ax.set_title('Scope boundary: reduced model misses high-delay mistiming (d44-d56)',fontsize=9.5)
    plt.tight_layout(); plt.savefig(os.path.join(OUT,'Figure_7.png'),dpi=300,bbox_inches='tight'); plt.close()

if __name__=='__main__':
    fig4(); fig5(); fig6(); print('Diagnostic figures (Figure_4, Figure_6, Figure_7) written to', OUT)
