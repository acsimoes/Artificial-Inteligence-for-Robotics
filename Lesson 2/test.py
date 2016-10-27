from math import exp, sqrt, pi

u = 10
var = 4
x = 8

f = 1/sqrt(2*pi*var)*exp(-0.5*(((x-u)**2)/var))

print f