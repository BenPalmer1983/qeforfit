import numpy
import matplotlib.pyplot as plt

d = numpy.genfromtxt('data.csv', delimiter=',')



plt.figure(figsize=(12,8))
plt.plot(d[:,0], d[:,1], '+')
plt.xlabel('Maximum Displacement from Perfect Crystal Location (Angstrom)')
plt.ylabel('Energy/Ry')
plt.title('')
plt.grid(True)
plt.savefig('plot.eps', format='eps')
plt.show()
plt.close('all') 

plt.figure(figsize=(12,8))
plt.plot(d[:,0], d[:,2], '+')
plt.xlabel('Maximum Displacement from Perfect Crystal Location (Angstrom)')
plt.ylabel('Temperature/K')
plt.title('Qeforfit Gheat')
plt.grid(True)
plt.savefig('plot.eps', format='eps')
plt.show()
plt.close('all') 
