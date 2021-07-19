from rand_dist import rand_dist
from rand_dist import Test_RandDist
import numpy

Test_RandDist.testRandGheat()

numpy.random.seed(20)
r = rand_dist()
r.gheat()
print(r.rng())
print(r.rng())
print(r.rng())
print(r.rng())
print(r.rng())
print(r.rng())





