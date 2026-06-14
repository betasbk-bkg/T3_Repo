"""(A) rate-damping 직접 증거: signed cross-track 오차의 진동에너지↓ + 트롤이 속도에 anti.
   (B) controller generality: SMOOTH(α)·LOOK 흔들어 효과 생존 확인."""
import numpy as np, adversary_ladder as AL
from adversary_ladder import Circle, Square

# --- Exp A: circle 전용, signed radial 오차 + 속도-반대상관 로깅 ---
def sim_log(traj,N,tr,seed,mode,delay_f=26,coh=1.0,R=10.0):
    rng=np.random.default_rng(seed); pos=traj.start(); vel=np.zeros(2); ph=[pos.copy()]
    pang=0.; cur_dir=np.array([1.,0.]); serr=[]; coss=[]; pub=[]
    for f in range(AL.FRAMES):
        if f%AL.VOTE_INT==0:
            di=max(0,len(ph)-1-delay_f); dp=ph[di]; _,arc=traj.closest(dp); lap=traj.at(arc+AL.LOOK)
            idir=lap-dp; n=np.linalg.norm(idir); idir=idir/n if n>1e-10 else idir
            iang=np.degrees(np.arctan2(idir[1],idir[0]))
            honest,nt=AL._honest_block(iang,pang,tr,N,rng); pang=iang
            troll_vec=np.zeros(2)
            if nt>0 and mode=='T3':
                base=iang if not pub else pub[-1]
                nc=int(np.floor(coh*nt)); nd=nt-nc
                tidx=np.concatenate([np.full(nc,AL.a2d(np.array([base+180.]))[0],int),
                                     rng.integers(0,8,nd) if nd>0 else np.array([],int)])
                troll_vec=AL.DIRS[tidx].mean(0) if nt>0 else np.zeros(2)
            elif nt>0:
                tidx=AL.a2d(iang+rng.uniform(-3,3,nt))
            else: tidx=np.array([],int)
            votes=np.concatenate([honest,tidx]); bl=AL.DIRS[votes].mean(0); nb=np.linalg.norm(bl)
            cur_dir=bl/nb if nb>1e-10 else cur_dir
            pub.append(np.degrees(np.arctan2(cur_dir[1],cur_dir[0])))
            # 트롤 기여 vs 현재 속도 방향의 cos (anti면 음수 = 속도damping)
            if mode=='T3' and np.linalg.norm(troll_vec)>1e-9 and np.linalg.norm(vel)>1e-9:
                coss.append(np.dot(troll_vec/np.linalg.norm(troll_vec), vel/np.linalg.norm(vel)))
        vel+=AL.SMOOTH*(cur_dir*AL.MSPD-vel); pos=pos+vel*AL.DT; ph.append(pos.copy())
        serr.append(np.linalg.norm(pos)-R)   # signed radial 오차
    serr=np.array(serr[120:])
    return dict(rms=float(np.sqrt(np.mean(serr**2))),
                osc=float(np.std(serr)),                      # 진동 에너지
                drms=float(np.sqrt(np.mean(np.diff(serr)**2))), # 오차 미분 RMS(진동성)
                cos_tv=float(np.mean(coss)) if coss else float('nan'))
def agg(traj,N,tr,mode,MC=20,**kw):
    rs=[sim_log(traj,N,tr,1000+i*31,mode,**kw) for i in range(MC)]
    return {k:np.nanmean([r[k] for r in rs]) for k in rs[0]}

print("=== (A) rate-damping 직접 증거 (circle N50 tr0.3 d26) ===")
h=agg(Circle(),50,0.30,'honest'); t=agg(Circle(),50,0.30,'T3')
print(f"  honest: RMS={h['rms']:.3f}  진동에너지(std)={h['osc']:.3f}  오차미분RMS={h['drms']:.4f}")
print(f"  T3    : RMS={t['rms']:.3f}  진동에너지(std)={t['osc']:.3f}  오차미분RMS={t['drms']:.4f}")
print(f"  => 진동에너지 {(t['osc']-h['osc'])/h['osc']*100:+.1f}%, 오차미분 {(t['drms']-h['drms'])/h['drms']*100:+.1f}%")
print(f"  => 트롤기여·속도 cos = {t['cos_tv']:+.3f}  (음수 = 속도 반대 = rate damping 정의)")

print("\n=== (B) controller generality (circle N50 tr0.3 d26): T3 이득이 살아남나 ===")
base_S, base_L = AL.SMOOTH, AL.LOOK
print(" [SMOOTH α 스윕]  (작을수록 관성↑/지연성↑)")
for s in [0.1,0.2,0.4]:
    AL.SMOOTH=s
    hh=agg(Circle(),50,0.30,'honest',MC=16); tt=agg(Circle(),50,0.30,'T3',MC=16)
    print(f"   α={s:.1f}: hon RMS={hh['rms']:.3f} T3={tt['rms']:.3f}  이득 {(tt['rms']-hh['rms'])/hh['rms']*100:+.1f}%")
AL.SMOOTH=base_S
print(" [LOOK ahead 스윕]  (클수록 예측/오버슈트↓)")
for L in [1.0,2.0,3.0]:
    AL.LOOK=L
    hh=agg(Circle(),50,0.30,'honest',MC=16); tt=agg(Circle(),50,0.30,'T3',MC=16)
    print(f"   LOOK={L:.1f}: hon RMS={hh['rms']:.3f} T3={tt['rms']:.3f}  이득 {(tt['rms']-hh['rms'])/hh['rms']*100:+.1f}%")
AL.LOOK=base_L
