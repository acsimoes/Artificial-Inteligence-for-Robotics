import random
def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"


def wheel_resampler(p, w):
    size = len(w)
    w_sum = sum(w)
    new_p = []
    w_norm = [i/w_sum for i in w]

    w_max = max(w_norm)
    index = int(round(random.random() * size))
    print index
    for i in range(10000):
        beta = random.uniform(0, 2*w_max)
        while w_norm[index] < beta:
            beta = beta - w_norm[index]
            index = (index + 1) % size

        new_p.append(p[index])

    return new_p

choices = [['a', 0.25], ['b',0.25], ['c', 0.25], ['d', 0.25]]
p = ['a','b','c','d']
w = [0.25, 0.25, 0.25, 0.25]

new_p = wheel_resampler(p, w)
for i in range(20):
    print weighted_choice(choices), new_p[i]

for i in range(len(p)):
    print 'number of occurances of ' + p[i] + ' is: ', new_p.count(p[i])