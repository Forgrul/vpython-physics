from vpython import *

g=9.8
size,m = 0.2, 1
L, k = 2, 150000
N = 2

scene = canvas(length=800, width=800, center=vec(0, -0.8, 0), background=vec(0,0.8,0.8), align='left')

pivots = []
for i in range(5):
    pivot = sphere(radius=0.06, pos=vec(-0.8+0.4*i, 0, 0), color=color.white)
    pivots.append(pivot)
    
strings = []
for i in range(5):
    string = cylinder(radius=0.04, pos=vec(-0.8+0.4*i, 0, 0), color=color.white)
    strings.append(string)
    
balls = []
for i in range(5):
    ball = sphere(radius=size, color=color.white)
    ball.pos = vec(-0.8+0.4*i, -L-m*g/k, 0)
    ball.v = vec(0,0,0)
    balls.append(ball)

for i in range(N):
    balls[i].pos += vec(-sqrt(L**2-1.95**2), 0.05, 0)

def af_col_v(m1, m2, v1, v2, x1, x2):
    v1_prime = v1 - 2*m2/(m1+m2)*(x1-x2) * dot(v1 - v2, x1 - x2) / (mag(x1-x2))**2
    v2_prime = v2 - 2*m1/(m1+m2)*(x2-x1) * dot(v2 - v1, x2 - x1) / (mag(x2-x1))**2
    return (v1_prime, v2_prime)

graph1 = graph(width=450, align='right')
funct1 = gcurve(graph=graph1, color=color.blue, width=4)
funct2 = gcurve(graph=graph1, color=color.red, width=4)
graph2 = graph(width=450, align='right')
funct3 = gcurve(graph=graph2, color=color.blue, width=4)
funct4 = gcurve(graph=graph2, color=color.red, width=4)

dt = 0.0001
t = 0
total_KE = total_U = 0
while True:
    rate(5000)
    t += dt
    
    KE = U = 0
    for i in range(5):
        strings[i].axis = balls[i].pos - strings[i].pos
        tension = -k * (mag(strings[i].axis) - L) * strings[i].axis.norm()
        balls[i].a = vec(0, -g, 0) + tension/m
        balls[i].v += balls[i].a * dt
        balls[i].pos += balls[i].v * dt
        
        if ((i <= 3 and mag(balls[i].pos - balls[i+1].pos) <= 2*size) and (dot(balls[i].pos - balls[i+1].pos, balls[i].v - balls[i+1].v) < 0)):
            balls[i].v, balls[i+1].v = af_col_v(m, m, balls[i].v, balls[i+1].v, balls[i].pos, balls[i+1].pos)
            
        KE += 0.5*m*(mag(balls[i].v)**2)
        U += m * g * (balls[i].pos.y -(-L-m*g/k))
            
    funct1.plot(t, KE)
    funct2.plot(t, U)
    total_KE += KE * dt
    total_U += U * dt
    funct3.plot(t, total_KE/t)
    funct4.plot(t, total_U/t)
    
    