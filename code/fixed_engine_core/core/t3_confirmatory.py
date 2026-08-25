import os
"""
t3_confirmatory.py  —  confirmatory full-grid on the real engine  [rev2]
================================================================
Run from the same folder as adversary_ladder.py; reuses the engine (honest block / trajectories / constants).
Key comparison = T3 vs the honest counterfactual (the same tr*N agents voting honestly). T0 is also reported.

[rev2 fixes]
  - seed: deterministic integer scheme (fixes hash() randomization bug -> run-to-run reproducibility)
  - ctrl_delay_f: control/feedback delay in frames (source of overshoot; original engine fixed DELAY_F=26).
                  this sweep varies the honest control delay -- a different axis from t3_obs_delay (observation delay).
  - t3_obs_delay: T3 observation delay (vote-rounds, default 1) exposed as a separate argument (same as original default).
Note: ctrl_delay_f=26, t3_obs_delay=1 reproduces the original adversary_ladder.sim(model='T3') setting.

Experiments:
  E1  control-delay sweep x trajectory x tr : {honest, T0, T3pub} -> delay-compensation curve + vs-honest gain (+T0 continuity)
  E2  coherence / partial collusion        : T3pub(c=0..1) vs honest
  E3  aggregation rule          : mean vs majority (continuous-aggregation specificity)
  E4  oracle vs public          : T3pub vs T3ora (self-inclusion)
Output: t3_confirmatory_results.json (+ console tables, bootstrap 95% CI)

Usage:
  python3 t3_confirmatory.py quick     # quick check (several minutes, machine-dependent)
  python3 t3_confirmatory.py full      # paper-grade (MC50; prints an ETA at start)
"""
import numpy as np, json, sys, time
import adversary_ladder as AL
from adversary_ladder import Circle, Square, Lemniscate, Zigzag

TRAJ = {'circle':Circle(),'square':Square(),'lemniscate':Lemniscate(),'zigzag':Zigzag()}
MODE_IDX = {'honest':0,'T0':1,'T3pub':2,'T3ora':3}
TRAJ_IDX = {'circle':0,'square':1,'lemniscate':2,'zigzag':3}

def sim_u(traj, N, tr, seed, mode, ctrl_delay_f=AL.DELAY_F, t3_obs_delay=1, coh=1.0, agg='mean'):
    """mode: honest(counterfactual)/T0/T3pub/T3ora. ctrl_delay_f: honest control delay (frames).
       t3_obs_delay: T3 observation delay (vote-rounds). coh: T3 collusion rate. agg: mean/majority."""
    rng=np.random.default_rng(seed); pos=traj.start(); vel=np.zeros(2); ph=[pos.copy()]
    pang=0.; cur_dir=np.array([1.,0.]); errs=np.empty(AL.FRAMES)
    pub_hist=[]; hon_hist=[]
    for f in range(AL.FRAMES):
        if f%AL.VOTE_INT==0:
            di=max(0,len(ph)-1-ctrl_delay_f); dp=ph[di]      # honest control delay (same mechanism as original DELAY_F)
            _,arc=traj.closest(dp); lap=traj.at(arc+AL.LOOK)
            idir=lap-dp; n=np.linalg.norm(idir); idir=idir/n if n>1e-10 else idir
            iang=np.degrees(np.arctan2(idir[1],idir[0]))
            honest,nt=AL._honest_block(iang,pang,tr,N,rng); pang=iang
            # T3 observation source: consensus direction (public or honest-only) from t3_obs_delay rounds earlier
            pubprev = pub_hist[-t3_obs_delay] if len(pub_hist)>=t3_obs_delay else None
            honprev = hon_hist[-t3_obs_delay] if len(hon_hist)>=t3_obs_delay else None
            if nt>0 and mode in ('T3pub','T3ora'):
                src = pubprev if mode=='T3pub' else honprev
                base = iang if src is None else src
                nc=int(np.floor(coh*nt)); nd=nt-nc
                troll=np.concatenate([np.full(nc,AL.a2d(np.array([base+180]))[0],int),
                                      rng.integers(0,8,nd) if nd>0 else np.array([],int)])
            elif nt>0 and mode=='T0':
                troll=rng.integers(0,8,nt)
            elif nt>0:                                        # honest counterfactual
                troll=AL.a2d(iang+rng.uniform(-3,3,nt))
            else: troll=np.array([],int)
            votes=np.concatenate([honest,troll])
            hb=AL.DIRS[honest].mean(0)                        # honest-only consensus (clean oracle source)
            hon_hist.append(np.degrees(np.arctan2(hb[1],hb[0])) if np.linalg.norm(hb)>1e-10 else iang)
            if agg=='mean':
                bl=AL.DIRS[votes].mean(0); nb=np.linalg.norm(bl); cur_dir=bl/nb if nb>1e-10 else cur_dir
            else:                                             # majority (discrete)
                cur_dir=AL.DIRS[np.bincount(votes,minlength=8).argmax()]
            pub_hist.append(np.degrees(np.arctan2(cur_dir[1],cur_dir[0])))
        vel+=AL.SMOOTH*(cur_dir*AL.MSPD-vel); pos=pos+vel*AL.DT; ph.append(pos.copy())
        cp,_=traj.closest(pos); errs[f]=np.linalg.norm(pos-cp)
    return float(np.sqrt(np.mean(errs**2)))

def _seed_base(traj_name,mode,tr,ctrl_delay_f,t3_obs_delay,coh,agg):
    """Deterministic integer seed base (run-to-run reproducibility; extends original i*31+... pattern)."""
    return (TRAJ_IDX[traj_name]*10_000_000 + MODE_IDX[mode]*1_000_000
            + int(round(tr*100))*10_000 + int(ctrl_delay_f)*100
            + int(round(coh*100)) + (0 if agg=='mean' else 5000)
            + t3_obs_delay*70_000)

def cell(traj_name,N,tr,mode,MC,**kw):
    base=_seed_base(traj_name,mode,tr,kw.get('ctrl_delay_f',AL.DELAY_F),
                    kw.get('t3_obs_delay',1),kw.get('coh',1.0),kw.get('agg','mean'))
    return np.array([sim_u(TRAJ[traj_name],N,tr,base+i*31,mode,**kw) for i in range(MC)])

_BOOT=np.random.default_rng(20260614)
def boot_ci(a,b,it=2000):
    na,nb=len(a),len(b); d=np.empty(it)
    for k in range(it): d[k]=b[_BOOT.integers(0,nb,nb)].mean()-a[_BOOT.integers(0,na,na)].mean()
    return float(np.percentile(d,2.5)),float(np.percentile(d,97.5))

def main(mode_run):
    QUICK=(mode_run!='full')
    MC      = 12 if QUICK else 50
    TRJS    = ['circle','zigzag'] if QUICK else ['circle','square','lemniscate','zigzag']
    DELAYS  = [0,18,34,52] if QUICK else [0,8,18,26,34,44,56,68]    # ctrl_delay_f (frame)
    TRS     = [0.30] if QUICK else [0.20,0.30,0.40]
    N=50
    res={'config':{'MC':MC,'trajs':TRJS,'ctrl_delays_frame':DELAYS,'trs':TRS,'N':N,
                   't3_obs_delay_rounds':1,'note':'ctrl_delay_f=honest control delay; original DELAY_F=26'},
         'E1':[],'E2':[],'E3':[],'E4':[]}
    nsim=len(TRJS)*(len(DELAYS)*len(TRS)*3 + 5 + 4 + 2)*MC
    print(f"[{mode_run}] MC={MC} | est. sim count={nsim} | ~{nsim*0.3/60:.0f} min (assuming 0.3s/sim)")
    t0=time.time()
    print("\n=== E1: control-delay sweep (T3pub vs honest counterfactual; T0 continuity) ===")
    for tn in TRJS:
        for tr in TRS:
            for d in DELAYS:
                h=cell(tn,N,tr,'honest',MC,ctrl_delay_f=d)
                a=cell(tn,N,tr,'T0',MC,ctrl_delay_f=d)
                b=cell(tn,N,tr,'T3pub',MC,ctrl_delay_f=d)
                lo,hi=boot_ci(h,b)
                res['E1'].append(dict(traj=tn,tr=tr,ctrl_delay_f=d,honest=float(h.mean()),
                    T0=float(a.mean()),T3=float(b.mean()),delta_T3_honest=float(b.mean()-h.mean()),
                    ci=[lo,hi],win=bool(hi<0)))
                print(f"  {tn:10} tr{tr:.2f} d{d:2d} | hon{h.mean():6.3f} T0{a.mean():6.3f} T3{b.mean():6.3f}"
                      f" | d(T3-hon){b.mean()-h.mean():+.3f}[{lo:+.3f},{hi:+.3f}] {'WIN' if hi<0 else ''}")
    print("\n=== E2: coherence / partial collusion (d=26) ===")
    for tn in TRJS:
        h=cell(tn,N,0.30,'honest',MC,ctrl_delay_f=26)
        for c in [0.0,0.25,0.5,0.75,1.0]:
            b=cell(tn,N,0.30,'T3pub',MC,ctrl_delay_f=26,coh=c)
            res['E2'].append(dict(traj=tn,coh=c,honest=float(h.mean()),T3=float(b.mean()),
                delta=float(b.mean()-h.mean())))
            print(f"  {tn:10} c{c:.2f} | T3{b.mean():6.3f} vs hon {(b.mean()-h.mean())/h.mean()*100:+.1f}%")
    print("\n=== E3: aggregation rule mean vs majority (d=26) ===")
    for tn in TRJS:
        for ag in ['mean','majority']:
            h=cell(tn,N,0.30,'honest',MC,ctrl_delay_f=26,agg=ag)
            b=cell(tn,N,0.30,'T3pub',MC,ctrl_delay_f=26,agg=ag)
            res['E3'].append(dict(traj=tn,agg=ag,honest=float(h.mean()),T3=float(b.mean()),
                delta_pct=float((b.mean()-h.mean())/h.mean()*100)))
            print(f"  {tn:10} {ag:9} | hon{h.mean():6.3f} T3{b.mean():6.3f} {(b.mean()-h.mean())/h.mean()*100:+.1f}%")
    print("\n=== E4: public vs oracle (d=26) ===")
    for tn in TRJS:
        bp=cell(tn,N,0.30,'T3pub',MC,ctrl_delay_f=26); bo=cell(tn,N,0.30,'T3ora',MC,ctrl_delay_f=26)
        res['E4'].append(dict(traj=tn,T3pub=float(bp.mean()),T3ora=float(bo.mean()),
            diff_pct=float((bo.mean()-bp.mean())/bp.mean()*100)))
        print(f"  {tn:10} | T3pub{bp.mean():6.3f} T3ora{bo.mean():6.3f} diff{(bo.mean()-bp.mean())/bp.mean()*100:+.1f}%")
    res['elapsed_sec']=time.time()-t0
    with open(os.path.join(os.path.dirname(__file__),'..','results','t3_confirmatory_results.json'),'w') as fp: json.dump(res,fp,indent=2,ensure_ascii=False)
    print(f"\nsaved: t3_confirmatory_results.json | {res['elapsed_sec']:.0f}s")

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'quick')
