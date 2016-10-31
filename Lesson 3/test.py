choices = [['a', 0.25], ['b',0.25], ['c', 0.25], ['d', 0.25]]


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

for i in range(20):
    print weighted_choice(choices)