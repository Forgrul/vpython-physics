from vpython import *
from numpy import *

N = 100
R, lamda = 1.0, 500E-9
d = 100E-6

dx, dy = d/N, d/N
scene1 = canvas(align = 'left', height=600, width=600, center = vector(N*dx/2, N*dy/2, 0))
scene2 = canvas(align = 'right', x=600, height=600, width=600, center = vector(N*dx/2, N*dy/2, 0))
scene1.lights, scene2.lights = [], []
scene1.ambient, scene2.ambient = color.gray(0.99), color.gray(0.99)
side = linspace(-0.01*pi, 0.01*pi, N)
x,y = meshgrid(side,side)

k = 2*pi / lamda
E_field = zeros((N,N))
for X_i in range(N):
    X = X_i * dx - d/2
    for Y_i in range(N):
        Y = Y_i * dy - d/2
        if X**2 + Y**2 <= (d/2)**2:
            E_field += 1/R * cos((k*x/R)*X + (k*y/R)*Y) * dx * dy

Inte = abs(E_field) ** 2
maxI = amax(Inte)
for i in range(N):
    for j in range(N):
        box(canvas = scene1, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx, \
            color=vector(Inte[i,j]/maxI,Inte[i,j]/maxI,Inte[i,j]/maxI))

for i in range(int(ceil(N/2)), N):
    if Inte[i, N//2] < Inte[i+1, N//2]:
        r_dark = x[N//2, i]
        print("Radius of the first dark ring:", r_dark)
        print("Theta =", r_dark/R)
        break
print("Rayleigh criterion Theta =", 1.22*lamda/d)

Inte = abs(E_field)
maxI = amax(Inte)
for i in range(N):
    for j in range(N):
        box(canvas = scene2, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx, \
            color=vector(Inte[i,j]/maxI,Inte[i,j]/maxI,Inte[i,j]/maxI))