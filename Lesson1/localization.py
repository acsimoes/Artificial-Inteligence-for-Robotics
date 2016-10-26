#Write code that outputs p after multiplying each entry
#by pHit or pMiss at the appropriate places. Remember that
#the red cells 1 and 2 are hits and the other green cells
#are misses.

n=5
p=[1./n]*n
pHit = 0.6
pMiss = 0.2

#Enter code here
world=['green','red','red','green','green']
measuraments=['green','red']

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (world[i]==Z)
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s=sum(q)
    for i in range(5):
        q[i]/=s
    return q

for i in range(len(measuraments)):
    p=sense(p,measuraments[i])

print p

def move(p, U):             #nice way to shift a list left or right in a circular way!
    n = U % len(p)
    q = p[-n:] + p[:-n]
    return q

print move(p,-2)