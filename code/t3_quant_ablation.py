"""결정적 실험: quantization 해상도 n 변화 -> T3 이득이 dead-zone(e*=L*tan(pi/n))처럼 줄어드나.
(A)dead-zone dither면 효과 ∝ dead-zone -> n↑서 급감. (B)rate-damping이면 n과 무관."""
import numpy as np, adversary_ladder as AL
from adversary_ladder import Circle, Square
def make_dirs(n):
    a=np.arange(n)*2*np.pi/n; return np.stack([np.cos(a),np.sin(a)],1), np.degrees(a)%360
def a2d_n(angles, DA):
    a=angles%360; d=np.abs(DA[None,:]-a[:,None]); d=np.minimum(d,360-d); return np.argmin(d,1)
def honest_angles(iang,pang,tr,N,rng):
    sc=(1-tr)/0.95; na=round(N*0.70*sc); ns=round(N*0.20*sc); nt=round(N*tr); no=max(0,N-na-ns-nt)
    ang=np.empty(na+ns+no); i=0
    ang[i:i+na]=iang+rng.uniform(-3,3,na); i+=na
    diff=iang-pang; diff=(diff+180)%360-180
    if ns>0: ang[i:i+ns]=pang+diff*(1-rng.uniform(0.2,0.5,ns)); i+=ns
    if no>0: ang[i:i+no]=iang+rng.uniform(-30,30,no); i+=no
    return ang[:i], nt
def sim_n(traj,N,tr,seed,mode,n,delay_f=26,coh=1.0):
    DIRS,DA=make_dirs(n); rng=np.random.default_rng(seed)
    pos=traj.start(); vel=np.zeros(2); ph=[pos.copy()]; pang=0.; cur_dir=np.array([1.,0.])
    errs=np.empty(AL.FRAMES); pub=[]
    for f in range(AL.FRAMES):
        if f%AL.VOTE_INT==0:
            di=max(0,len(ph)-1-delay_f); dp=ph[di]; _,arc=traj.closest(dp); lap=traj.at(arc+AL.LOOK)
            idir=lap-dp; nn=np.linalg.norm(idir); idir=idir/nn if nn>1e-10 else idir
            iang=np.degrees(np.arctan2(idir[1],idir[0]))
            hang,nt=honest_angles(iang,pang,tr,N,rng); pang=iang
            hidx=a2d_n(hang,DA)
            if nt>0 and mode=='T3':
                base=iang if not pub else pub[-1]
                nc=int(np.floor(coh*nt)); nd=nt-nc
                tidx=np.concatenate([a2d_n(np.full(nc,base+180.),DA),
                                     rng.integers(0,n,nd) if nd>0 else np.array([],int)])
            elif nt>0:  # honest 반사실
                tidx=a2d_n(iang+rng.uniform(-3,3,nt),DA)
            else: tidx=np.array([],int)
            votes=np.concatenate([hidx,tidx]); bl=DIRS[votes].mean(0); nb=np.linalg.norm(bl)
            cur_dir=bl/nb if nb>1e-10 else cur_dir
            pub.append(np.degrees(np.arctan2(cur_dir[1],cur_dir[0])))
        vel+=AL.SMOOTH*(cur_dir*AL.MSPD-vel); pos=pos+vel*AL.DT; ph.append(pos.copy())
        cp,_=traj.closest(pos); errs[f]=np.linalg.norm(pos-cp)
    return float(np.sqrt(np.mean(errs**2)))
def cell(traj,N,tr,mode,n,MC=24): return np.mean([sim_n(traj,N,tr,1000+n*7+i*31,mode,n) for i in range(MC)])
print("dead-zone 폭 e*=L*tan(pi/n):", {n:round(AL.LOOK*np.tan(np.pi/n),3) for n in [8,16,32]})
print("\n(A)dead-zone면 효과 n↑서 급감 / (B)rate-damping이면 n무관. delay26 tr0.3")
for tn,t in [('circle',Circle()),('square',Square())]:
    print(f"\n== {tn} ==")
    print(f"{'n':>3} {'e*':>6} | {'honest':>7} {'T3':>7} | {'이득%':>7}")
    for n in [8,16,32]:
        h=cell(t,50,0.30,'honest',n); b=cell(t,50,0.30,'T3',n); adv=(h-b)/h*100
        print(f"{n:3d} {AL.LOOK*np.tan(np.pi/n):6.3f} | {h:7.3f} {b:7.3f} | {adv:+7.1f}")
