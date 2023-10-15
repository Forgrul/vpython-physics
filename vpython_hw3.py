from vpython import *
import numpy as np

A, N, omega = 0.10, 50, 2*pi/1.0
size, m, k, d = 0.06, 0.1, 10.0, 0.4

# scene = canvas(title='Spring Wave', width=800, height=300, background=vec(0.5,0.5,0), center = vec((N-1)*d/2, 0, 0))
# balls = [sphere(radius=size, color=color.red, pos=vector(i*d, 0, 0), v=vector(0,0,0)) for i in range(N)]
# springs = [helix(radius = size/2.0, thickness = d/15.0, pos=vector(i*d, 0, 0), axis=vector(d,0,0)) for i in range(N-1)]

# c = curve([vector(i*d, 1.0, 0) for i in range(N)], color=color.black)
graph_dr = graph(width=800, align='left', title='Phonon dispersion relationship', xtitle='Wavevector', ytitle='Angular Frequency', background=vec(0.3, 0.7, 0.4))
dr = gcurve(color=color.blue, graph=graph_dr)

for n in range(1, N//2):

    Unit_K = 2 * pi/(N*d)
    Wavevector = n * Unit_K
    phase = Wavevector * arange(N) * d
    ball_pos, ball_orig, ball_v, spring_len = np.arange(N)*d + A*np.sin(phase), np.arange(N)*d, np.zeros(N), np.ones(N)*d

    t, dt = 0, 0.001
    prev_v = ball_v[1]
    reach_max_times = 0

    while True:
        
        rate(10000)
        t += dt
        
        spring_len[:-1] = ball_pos[1:] - ball_pos[:-1]
        spring_len[-1] = ball_pos[0] + N*d - ball_pos[-1]
        ball_v[0] += (-k * (spring_len[-1] - d) / m + k * (spring_len[0] - d) / m) * dt
        ball_v[1:] += (-k * (spring_len[:-1] - d) / m + k * (spring_len[1:] - d) / m) * dt
        
        ball_pos += ball_v * dt
            
        # for i in range(N):
        #     balls[i].pos.x = ball_pos[i]
        # for i in range(N-1):
        #     springs[i].pos = balls[i].pos
        #     springs[i].axis = balls[i+1].pos - balls[i].pos

        # ball_disp = ball_pos - ball_orig
        # for i in range(N):
        #     c.modify(i, y = ball_disp[i]*4+1)

        if prev_v > 0 and ball_v[1] <= 0:
            reach_max_times += 1
            if reach_max_times == 1:
                t0 = t
            elif reach_max_times == 2:
                period = t - t0
                omega = 2*pi/period
                dr.plot(pos=(Wavevector, omega))
                break
        prev_v = ball_v[1]

