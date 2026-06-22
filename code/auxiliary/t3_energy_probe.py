import sys, copy, json, numpy as np
sys.path.insert(0,'/mnt/data')
import adversary_ladder as AL
from adversary_ladder import Circle, Square, Lemniscate, Zigzag

TRAJ={'circle':Circle(), 'square':Square(), 'lemniscate':Lemniscate(), 'zigzag':Zigzag()}

def tangent_normal(traj, arc, eps=0.15):
    p1=traj.at(arc+eps); p0=traj.at(arc-eps)
    t=p1-p0; n=np.linalg.norm(t)
    if n<1e-9: return np.array([1.,0.]), np.array([0.,1.])
    t=t/n; return t, np.array([-t[1], t[0]])

def signed_error_and_normal(traj, pos):
    cp,arc=traj.closest(pos)
    if isinstance(traj, Circle):
        r=np.linalg.norm(pos); nvec=pos/r if r>1e-12 else np.array([1.,0.])
        return r-traj.R, nvec, cp, arc
    _,nvec=tangent_normal(traj, arc)
    e=float(np.dot(pos-cp,nvec))
    return e, nvec, cp, arc

def sim_energy_probe(traj, N=50, tr=0.30, seed=0, ctrl_delay_f=26, coh=1.0, mode='T3pub'):
    rng=np.random.default_rng(seed)
    pos=traj.start(); vel=np.zeros(2); ph=[pos.copy()]
    pang=0.; cur_dir=np.array([1.,0.]); cf_dir=np.array([1.,0.])
    pub=[]; hon=[]
    errs=[]; es=[]; edots=[]
    # core diagnostics
    energy_power=[]      # e * delta_v_perp; <0 means T3 decreases error energy relative to CF
    abs_error_power=[]   # sign(e)*delta_v_perp; <0 means one-step absolute error reduction
    vel_damp_power=[]    # edot * delta_v_perp; <0 means velocity damping relative to CF
    cmd_angle=[]; raw_cos=[]
    delta_perps=[]; delta_norms=[]
    tail_marker=[]
    for f in range(AL.FRAMES):
        if f%AL.VOTE_INT==0:
            di=max(0,len(ph)-1-ctrl_delay_f); dp=ph[di]
            _,arc=traj.closest(dp); lap=traj.at(arc+AL.LOOK)
            idir=lap-dp; nn=np.linalg.norm(idir); idir=idir/nn if nn>1e-10 else idir
            iang=np.degrees(np.arctan2(idir[1],idir[0]))
            honest,nt=AL._honest_block(iang,pang,tr,N,rng); pang=iang
            # Use same state right after honest block to generate paired honest counterfactual trolls
            state=copy.deepcopy(rng.bit_generator.state)
            rng_cf=np.random.default_rng(); rng_cf.bit_generator.state=copy.deepcopy(state)
            pubprev=pub[-1] if pub else None
            honprev=hon[-1] if hon else None
            if nt>0 and mode in ('T3pub','T3ora'):
                src=pubprev if mode=='T3pub' else honprev
                base=iang if src is None else src
                nc=int(np.floor(coh*nt)); nd=nt-nc
                tidx=np.concatenate([np.full(nc,AL.a2d(np.array([base+180.]))[0],int),
                                     rng.integers(0,8,nd) if nd>0 else np.array([],int)])
                cfidx=AL.a2d(iang+rng_cf.uniform(-3,3,nt))
            elif nt>0:
                tidx=AL.a2d(iang+rng.uniform(-3,3,nt))
                cfidx=tidx.copy()
            else:
                tidx=np.array([],int); cfidx=np.array([],int)
            votes=np.concatenate([honest,tidx]); votes_cf=np.concatenate([honest,cfidx])
            bl=AL.DIRS[votes].mean(0); nb=np.linalg.norm(bl)
            cur_dir=bl/nb if nb>1e-10 else cur_dir
            blcf=AL.DIRS[votes_cf].mean(0); nbcf=np.linalg.norm(blcf)
            cf_dir=blcf/nbcf if nbcf>1e-10 else cf_dir
            # honest-only consensus for oracle history
            hb=AL.DIRS[honest].mean(0); hn=np.linalg.norm(hb)
            hon.append(np.degrees(np.arctan2(hb[1],hb[0])) if hn>1e-10 else iang)
            pub.append(np.degrees(np.arctan2(cur_dir[1],cur_dir[0])))
            if np.linalg.norm(vel)>1e-9:
                # raw minority vector can be stored too
                tv=AL.DIRS[tidx].mean(0) if len(tidx)>0 else np.zeros(2)
                if np.linalg.norm(tv)>1e-9:
                    raw_cos.append(float(np.dot(tv/np.linalg.norm(tv), vel/np.linalg.norm(vel))))
        # diagnostics at current frame, before update
        e,nvec,cp,arcnow=signed_error_and_normal(traj,pos)
        edot=float(np.dot(vel,nvec))
        delta_v_next=AL.SMOOTH*AL.MSPD*(cur_dir-cf_dir)
        dvp=float(np.dot(delta_v_next,nvec))
        energy_power.append(e*dvp)
        abs_error_power.append(np.sign(e)*dvp if abs(e)>1e-12 else 0.0)
        vel_damp_power.append(edot*dvp)
        delta_perps.append(dvp); delta_norms.append(float(np.linalg.norm(delta_v_next)))
        # actual T3 update
        vel+=AL.SMOOTH*(cur_dir*AL.MSPD-vel); pos=pos+vel*AL.DT; ph.append(pos.copy())
        cp2,_=traj.closest(pos); errs.append(np.linalg.norm(pos-cp2)); es.append(e); edots.append(edot)
    sl=slice(120,None)
    arr=lambda x: np.array(x)[sl]
    errs=arr(errs); es=arr(es); edots=arr(edots); ep=arr(energy_power); ap=arr(abs_error_power); vp=arr(vel_damp_power); dp=arr(delta_perps); dn=arr(delta_norms)
    denomE=np.mean(np.abs(es*dp))+1e-12
    denomA=np.mean(np.abs(dp))+1e-12
    denomV=np.mean(np.abs(edots*dp))+1e-12
    return {
        'rmse':float(np.sqrt(np.mean(errs**2))),
        'signed_rms':float(np.sqrt(np.mean(es**2))),
        'osc_std':float(np.std(es)),
        'edot_rms':float(np.sqrt(np.mean(np.diff(es)**2))),
        # positive = T3 locally reduces signed-error energy/abs error/velocity compared with paired CF
        'energy_relief':float(-np.mean(ep)/denomE),
        'abs_relief':float(-np.mean(ap)/denomA),
        'vel_damping':float(-np.mean(vp)/denomV),
        'mean_energy_power':float(np.mean(ep)),
        'mean_abs_power':float(np.mean(ap)),
        'mean_vel_power':float(np.mean(vp)),
        'delta_norm':float(np.mean(dn)),
        'delta_perp_abs':float(np.mean(np.abs(dp))),
        'raw_cos_vel':float(np.mean(raw_cos)) if raw_cos else float('nan')
    }

def run(traj_name='circle', MC=10, tr=0.30, delays=(0,8,18,26,34,44,56,68)):
    traj=TRAJ[traj_name]
    out=[]
    for d in delays:
        rows=[sim_energy_probe(traj, seed=5_000_000 + d*1000 + i*31, ctrl_delay_f=d, tr=tr) for i in range(MC)]
        avg={k:float(np.nanmean([r[k] for r in rows])) for k in rows[0]}
        avg['delay']=d; out.append(avg)
        print(f"{traj_name:10} d{d:2d} rmse={avg['rmse']:.3f} Erelief={avg['energy_relief']:+.3f} Arelief={avg['abs_relief']:+.3f} Vdamp={avg['vel_damping']:+.3f} osc={avg['osc_std']:.3f} edot={avg['edot_rms']:.4f} rawcos={avg['raw_cos_vel']:+.3f}")
    return out

if __name__=='__main__':
    MC=int(sys.argv[1]) if len(sys.argv)>1 else 10
    res={}
    for tn in ['circle']:
        res[tn]=run(tn,MC=MC)
    with open('/mnt/data/t3_energy_probe_rows.json','w') as f: json.dump(res,f,indent=2)
