"""Analytic stability-boundary statement + numerical d* (companion-matrix) cross-check.
Closed loop (linear delay model):
  v_{t+1}=(1-a)v_t + a*U_t,   e_{t+1}=(1-L)e_t + D*v_{t+1}
  honest: U=-g*e_{t-d}        T3: U=-(1-p)g*e_{t-d} - p*k*v_t
Characteristic equation:  (z-(1-L)) (z-(1-a)+a*p*k) z^{d-1} + a(1-p)g D = 0
Boundary (z=e^{j.theta}): |.|=a(1-p)gD, arg(.)+(d-1)theta=pi  =>  each theta -> (g,d) boundary point.
"""
import numpy as np
def boundary_point(theta, a, L, D, p, k):
    z=np.exp(1j*theta)
    b=(1-a)+a*p*k           # T3 damping pole (honest: p=0 -> b=1-a)
    F=(z-(1-L))*(z-b)        # core factor without the z^{d-1} term
    mag=abs(F); ang=np.angle(F)
    # |F|*|z^{d-1}| = a(1-p)gD  => g = mag/(a(1-p)D)
    g=mag/(a*(1-p)*D)
    # arg(F)+(d-1)theta = pi  => d = 1 + (pi-arg(F))/theta
    d=1+(np.pi-ang)/theta
    return g,d
def crit_delay_analytic(g_target, a,L,D,p,k):
    # sweep theta to trace the boundary curve, then read the critical d at g_target
    best=None
    for th in np.linspace(0.01,np.pi,4000):
        g,d=boundary_point(th,a,L,D,p,k)
        if d>0 and abs(g-g_target)<0.01:
            if best is None or d<best: best=d
    return best
# --- numerical d* (companion matrix) recomputation ---
def companion(d,p,k,g,a,L,D):
    n=d+2; A=np.zeros((n,n))
    cE=-(1-p)*g; cV=-p*k
    A[1,1]=(1-a)+a*cV; A[1,d+1]=a*cE
    A[0,0]=(1-L); A[0,1]=D*A[1,1]; A[0,d+1]=D*A[1,d+1]
    if n>2: A[2,0]=1.0
    for kk in range(3,n): A[kk,kk-1]=1.0
    return A
def dstar_num(p,k,g,a=0.2,L=0.0,D=1.0):
    last=-1
    for d in range(0,200):
        if max(abs(np.linalg.eigvals(companion(d,p,k,g,a,L,D))))<=1+1e-9: last=d
        else: break
    return last
a,L,D=0.2,0.0,1.0; p,k=0.30,0.5
print("=== analytic boundary vs numerical d* (a=0.2,leak=0,D=1; T3: p=0.3,k=0.5) ===")
print(f"{'g':>5} | {'honest d* (num)':>16} {'analytic d':>12} | {'T3 d* (num)':>13} {'analytic d':>12}")
for g in [0.25,0.30,0.40,0.50]:
    dh_n=dstar_num(0.0,0.0,g,a,L,D); dt_n=dstar_num(p,k,g,a,L,D)
    dh_a=crit_delay_analytic(g,a,L,D,0.0,0.0); dt_a=crit_delay_analytic(g,a,L,D,p,k)
    print(f"{g:5.2f} | {dh_n:16d} {(f'{dh_a:.1f}' if dh_a else 'NA'):>12} | {dt_n:13d} {(f'{dt_a:.1f}' if dt_a else 'NA'):>12}")
print("\n=== statement (analytic): the two T3 channels enlarge the small-signal stability region ===")
print("  (a) effective gain: g_eff=(1-p)g < g  -> constant term a(1-p)gD decreases -> larger d* at the same g")
print("  (b) damping pole: (1-a) -> (1-a)-a*p*k (moves inside the unit circle) -> higher damping ratio")
# separate the two channels
print("\n  channel separation (g=0.40):")
print(f"   honest d*           = {dstar_num(0.0,0.0,0.40,a,L,D)}")
print(f"   (a) gain only (p=.3,k=0) = {dstar_num(0.30,0.0,0.40,a,L,D)}")
print(f"   (b) gain+damping (p=.3,k=0.5) = {dstar_num(0.30,0.5,0.40,a,L,D)}  <- combined)")
