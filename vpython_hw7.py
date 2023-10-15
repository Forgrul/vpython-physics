from vpython import *

fd = 120 # 120Hz
R = 30
L = 200e-3
C = 20e-6
X_L = 2*pi*fd*L
X_C = 1/(2*pi*fd*C)
Z = sqrt(R**2 + (X_L - X_C)**2)
T = 1/fd
I = 0
Q = 0
I_max = 0
I_0_t = 0
V_0_t = 0

t = 0
dt = 1.0/(fd * 5000) # 5000 simulation points per cycle

scene1 = graph(align = 'left', xtitle='t', ytitle='i (A) blue, v (100V) red,', background=vector(0.2, 0.6, 0.2))
scene2 = graph(align = 'left', xtitle='t', ytitle='Energy (J)', background=vector(0.2, 0.6, 0.2))

i_t = gcurve(color=color.blue, graph = scene1)
v_t = gcurve(color=color.red, graph = scene1)
E_t = gcurve(color=color.red, graph = scene2)

I_before = V_before = 0
while t <= 12 * T:

    V = 36*sin(2*pi*fd*t)
    V_R = I * R
    V_C = Q / C
    V_L = V - V_R - V_C
    I += V_L / L * dt
    Q += I * dt

    i_t.plot(t, I)
    v_t.plot(t, V / 100)

    E = 0.5*L*I**2 + 0.5*Q**2/C
    E_t.plot(t, E)

    if t >= 9 * T:
        if I >= I_max:
            I_max = I
        if I_0_t == 0:
            if I_before > 0 and I < 0:
                I_0_t = t
            I_before = I
        if V_0_t == 0:
            if V_before > 0 and V < 0:
                V_0_t = t
            V_before = V

    t += dt

V = 0
target_E = 0.1 * E
target_t = 0
while t <= 20 * T:
    V_R = I * R
    V_C = Q / C
    V_L = V - V_R - V_C
    I += V_L / L * dt
    Q += I * dt

    i_t.plot(t, I)
    v_t.plot(t, V / 100)

    E = 0.5*L*I**2 + 0.5*Q**2/C
    E_t.plot(t, E)

    if target_t == 0 and E <= target_E:
        target_t = t
    
    t += dt


print(f"Amplitude of I = {I_max} A")
print(f"Phase constant = {2*pi/T*abs(I_0_t - V_0_t) * 180/pi} degree")
print(f"Theoretical amplitude of I = {36 / Z} A")
print(f"Theoretical phase constant = {acos(R/Z) * 180 / pi} degree")
print(f"The time such that the energy decays to 10% is at {target_t} s.")