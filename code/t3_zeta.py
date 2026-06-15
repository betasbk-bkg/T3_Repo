"""Effective damping ratio zeta via the log-decrement of the signed-error autocorrelation.
Underdamped 2nd-order: autocorrelation peaks decay as exp(-zeta*w*tau) -> log-decrement delta -> zeta=delta/sqrt((2pi)^2+delta^2)."""
import numpy as np, adversary_ladder as AL
from adversary_ladder import Circle
def sim_serr(traj,N,tr,seed,mode,delay_f=26,coh=1.0,R=10.0):
    rng=np.random.default_rng(seed); pos=traj.start(); vel=np.zeros(2); ph=[pos.copy()]
    pang=0.; cur_dir=np.array([1.,0.]); serr=np.empty(AL.FRAMES); pub=[]
    for f in range(AL.FRAMES):
        if f%AL.VOTE_INT==0:
            di=max(0,len(ph)-1-delay_f); dp=ph[di]; _,arc=traj.closest(dp); lap=traj.at(arc+AL.LOOK)
            idir=lap-dp; n=np.linalg.norm(idir); idir=idir/n if n>1e-10 else idir
            iang=np.degrees(np.arctan2(idir[1],idir[0]))
            honest,nt=AL._honest_block(iang,pang,tr,N,rng); pang=iang
            if nt>0 and mode=='T3':
                base=iang if not pub else pub[-1]; nc=int(np.floor(coh*nt)); nd=nt-nc
                tidx=np.concatenate([np.full(nc,AL.a2d(np.array([base+180.]))[0],int),
                                     rng.integers(0,8,nd) if nd>0 else np.array([],int)])
            elif nt>0: tidx=AL.a2d(iang+rng.uniform(-3,3,nt))
            else: tidx=np.array([],int)
            votes=np.concatenate([honest,tidx]); bl=AL.DIRS[votes].mean(0); nb=np.linalg.norm(bl)
            cur_dir=bl/nb if nb>1e-10 else cur_dir
            pub.append(np.degrees(np.arctan2(cur_dir[1],cur_dir[0])))
        vel+=AL.SMOOTH*(cur_dir*AL.MSPD-vel); pos=pos+vel*AL.DT; ph.append(pos.copy())
        serr[f]=np.linalg.norm(pos)-R
    return serr[120:]
def zeta_from_series(e):
    e=e-e.mean(); r=np.correlate(e,e,'full'); r=r[len(r)//2:]; r=r/r[0]
    # find positive autocorrelation peaks
    pk=[]
    for i in range(1,len(r)-1):
        if r[i]>r[i-1] and r[i]>r[i+1] and r[i]>0.02: pk.append((i,r[i]))
        if len(pk)>=4: break
    if len(pk)<2: return np.nan
    # log-decrement from consecutive peak ratios (averaged)
    deltas=[]
    for j in range(len(pk)-1):
        if pk[j][1]>0 and pk[j+1][1]>0: deltas.append(np.log(pk[j][1]/pk[j+1][1]))
    if not deltas: return np.nan
    d=np.mean(deltas); return d/np.sqrt((2*np.pi)**2+d**2)
def zeta_avg(mode,MC=20):
    zs=[zeta_from_series(sim_serr(Circle(),50,0.30,1000+i*31,mode)) for i in range(MC)]
    zs=[z for z in zs if not np.isnan(z)]; return np.mean(zs),np.std(zs),len(zs)
print("=== effective damping ratio zeta (circle N50 tr0.3 d26, log-decrement) ===")
zh,sh,nh=zeta_avg('honest'); zt,st,nt=zeta_avg('T3')
print(f"  honest: zeta = {zh:.3f} +/- {sh:.3f}  (n={nh})")
print(f"  T3    : zeta = {zt:.3f} +/- {st:.3f}  (n={nt})")
print(f"  => d_zeta = {zt-zh:+.3f}  ({(zt-zh)/zh*100:+.0f}%)  {'T3 higher damping ratio' if zt>zh else 'inconclusive'}")
