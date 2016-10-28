#For this problem, you aren't writing any code.
#Instead, please just change the last argument
#in f() to maximize the output.

from math import *

def f(mu, sigma2, x):
    return 1/sqrt(2.*pi*sigma2) * exp(-.5*(x-mu)**2 / sigma2)

print f(10.,4.,10.) #Change the 8. to something else!

def update(mean1, var1, mean2, var2):
    newMean = (var2*mean1 + var1*mean2) / (var1 + var2)
    newVar = 1 / (1/var1 + 1/var2)
    return [newMean, newVar]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

def kalman_filter(mean0, var0, measurements, measurement_var, motion, motion_var):
    num_iter = len(measurements)
    mean = mean0
    var = var0
    for i in range(num_iter):
        [mean, var] = update(mean,var,measurements[i],measurement_var)
        [mean, var] = predict(mean,var,motion[i],motion_var)
    return [mean,var]

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0.
sig = 10000.

print kalman_filter(mu,sig,measurements,measurement_sig,motion,motion_sig)
