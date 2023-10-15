from vpython import *

g = 9.8
size = 0.25
theta = pi / 4
C_drag = 0.9
proportional_const = 0.3

scene = canvas(width=500, center=vec(0, 6, 0), background=vec(.3, .5, .5), align='left')
floor = box(length=40, height=0.01, width=10, color=color.blue)
ball = sphere(radius=size, color=color.red, make_trail=True, trail_radius=size/3)
arr = arrow(color=color.yellow, shaftwidth = 0.1)
gph = graph(width=450, align='right', xtitle='time(s)', ytitle='speed(m/s)')
func = gcurve(graph = gph, width=1, color=color.blue)

ball.pos = vec(-15, size, 0)
ball.v = vec(20*cos(theta), 20*sin(theta), 0)
arr.pos = ball.pos
arr.axis = proportional_const * ball.v

dt = 0.001
time = 0
largest_height = 0
total_distance = 0
counter = 0  # count the number of times the ball hits the ground
while counter < 3:
    
    rate(1/dt)
    time += dt
    
    ball.pos += ball.v * dt
    ball.v += (vec(0, -g, 0) * dt - C_drag * ball.v * dt)
    
    arr.pos = ball.pos
    arr.axis =  proportional_const * ball.v
    
    if ball.pos.y <= size:
        ball.v.y = -ball.v.y
        counter += 1
    
    if ball.pos.y > largest_height:
        largest_height = ball.pos.y
    total_distance += ball.v.mag * dt
    
    func.plot(pos=(time, ball.v.mag))

msg3 = text(text="Displacement = "+str(ball.pos.x - (-15)), pos=vec(-15.0, 15.5, 0))
msg2 = text(text="Total distance = "+str(total_distance), pos=vec(-15.0, 14, 0)) 
msg1 = text(text="Largest height = "+str(largest_height), pos=vec(-15.0, 12.5, 0))
