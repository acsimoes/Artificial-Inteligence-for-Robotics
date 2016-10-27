#Code for a very simple example of discrete localization
#Uses both sensorial information represented by the sense
#function as well as simulates movement of the robot through
#function move.

n=5
p=[1./n]*n
p=[0,1,0,0,0]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

world=['green','red','red','green','green']
measurements = ['red', 'green']
motions = [1,-1]

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (world[i]==Z)
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s=sum(q)
    for i in range(5):
        q[i]/=s
    return q

def circular_shift(p, U):             #nice way to shift a list left or right in a circular way!
    n = U % len(p)
    q = p[-n:] + p[:-n]
    return q

def move(p, U):
    q = [0]*len(p)
    for i in range(len(p)):
        q[i] += (p[i-U%len(p)] * pExact + p[i-(U-1)%len(p)] * pOvershoot + p[i-(U+1)%len(p)] * pUndershoot)
    return q

for i in range(len(motions)):
    p = sense(p,measurements[i])
    p = move(p, motions[i])

print p