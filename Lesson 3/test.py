choices = [['a', 0.25], ['b',0.25], ['c', 0.25], ['d', 0.25]]
p = ['a','b','c','d']
w = [0.25,0.25,0.25,0.25]


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
    index = [i for i in range(size)]
    new_p = []

    for i in range(20):
        j = i % size
        beta = random.uniform(0, 1)
        while (w[index[j]] / w_sum) < beta:
            beta = beta - w[index[j]]
            j = (j + 1) % size

        new_p.append(p[index[j]])

    return new_p

new_p = wheel_resampler(p,w)
for i in range(20):
    print weighted_choice(choices), new_p[i]