"""(1) 해석적 안정경계 정리 + 수치 d*(companion) 대조 검증.
폐루프(선형 지연모델):
  v_{t+1}=(1-a)v_t + a*U_t,   e_{t+1}=(1-L)e_t + D*v_{t+1}
  honest: U=-g*e_{t-d}        T3: U=-(1-p)g*e_{t-d} - p*k*v_t
특성방정식:  (z-(1-L)) (z-(1-a)+a*p*k) z^{d-1} + a(1-p)g D = 0
경계(z=e^{jθ}): |.|=a(1-p)gD,  arg(.)+(d-1)θ=π  =>  각 θ -> (g,d) 경계점.
"""
import numpy as np
def boundary_point(theta, a, L, D, p, k):
    z=np.exp(1j*theta)
    b=(1-a)+a*p*k           # T3 댐핑 극 (honest는 p=0 -> b=1-a)
    F=(z-(1-L))*(z-b)        # z^{d-1} 곱 빼고 핵심
    mag=abs(F); ang=np.angle(F)
    # |F|*|z^{d-1}| = a(1-p)gD  => g = mag/(a(1-p)D)
    g=mag/(a*(1-p)*D)
    # arg(F)+(d-1)θ = π  => d = 1 + (π-arg(F))/θ
    d=1+(np.pi-ang)/theta
    return g,d
def crit_delay_analytic(g_target, a,L,D,p,k):
    # θ 스윕해서 경계곡선 그리고, g_target에서의 임계 d 읽기
    best=None
    for th in np.linspace(0.01,np.pi,4000):
        g,d=boundary_point(th,a,L,D,p,k)
        if d>0 and abs(g-g_target)<0.01:
            if best is None or d<best: best=d
    return best
# --- 수치 d* (게이트4 companion) 재계산 ---
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
print("=== 해석적 경계 vs 수치 d* 대조 (a=0.2,leak=0,D=1; T3: p=0.3,k=0.5) ===")
print(f"{'g':>5} | {'honest d* (수치)':>16} {'해석경계 d':>12} | {'T3 d* (수치)':>13} {'해석경계 d':>12}")
for g in [0.25,0.30,0.40,0.50]:
    dh_n=dstar_num(0.0,0.0,g,a,L,D); dt_n=dstar_num(p,k,g,a,L,D)
    dh_a=crit_delay_analytic(g,a,L,D,0.0,0.0); dt_a=crit_delay_analytic(g,a,L,D,p,k)
    print(f"{g:5.2f} | {dh_n:16d} {(f'{dh_a:.1f}' if dh_a else 'NA'):>12} | {dt_n:13d} {(f'{dt_a:.1f}' if dt_a else 'NA'):>12}")
print("\n=== 정리(해석적): T3 항의 두 채널이 안정영역을 *해석적으로* 확장 ===")
print("  (a) 유효이득: g_eff=(1-p)g < g  -> 특성식 상수항 a(1-p)gD 감소 -> 경계 g↑(=같은 g서 d*↑)")
print("  (b) 댐핑극:   pole (1-a) -> (1-a)-a*p*k  (단위원 안쪽으로) -> 감쇠비↑")
# 두 채널 분리 검증
print("\n  채널 분리 (g=0.40):")
print(f"   honest d*           = {dstar_num(0.0,0.0,0.40,a,L,D)}")
print(f"   (a)이득만 (p=.3,k=0) = {dstar_num(0.30,0.0,0.40,a,L,D)}")
print(f"   (b)댐핑만 (p=.3 형식, 이득 보정) = {dstar_num(0.30,0.5,0.40,a,L,D)}  <- 둘 합)")
