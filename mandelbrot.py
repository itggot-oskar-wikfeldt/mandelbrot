import numpy as np
import matplotlib
import time
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage
from matplotlib import cm

#fig, ax = plt.subplots(figsize=(8, 8))   
fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(8, 8))

def small_range(start, end, step):
    while start <= end:
        yield start
        start += step

for axc in axs:
    for ax in axc:
        ax.axhline(0, color='black', lw=1)
        ax.axvline(0, color='black', lw=1)
        ax.set_xticks([-2, 0, 2])
        ax.set_yticks([-2, 0, 2])

ax = axs[0][0]
ax.set_title('NonUniformImage')

plt.xlabel('Real')
plt.ylabel('Imaginary')

STEP = 0.002
MIN = -2
MAX = 2

c_numbers = []
prevtime = time.time()
for r in small_range(MIN, MAX, STEP):
    for i in small_range(MIN, MAX, STEP):
        c = complex(r, i)
    
        z = 0
        for i in range(512):
            if abs(z) > 2:
                break
            z = z**2 + c
        if abs(z) < 2:
            c_numbers.append(c)
print(time.time() - prevtime)

im = NonUniformImage(ax, interpolation='bilinear', extent=(MIN, MAX, MIN, MAX),
                     cmap=cm.Purples)

num_of_points = int(abs(MIN-MAX)/STEP)
x = y = np.linspace(MIN, MAX, abs(MIN-MAX)/STEP)
z = np.ndarray(shape=(num_of_points, num_of_points), buffer=np.array((num_of_points**2)*[0]), dtype=int)
for c in c_numbers:
    z[int((c.imag-MIN)/STEP), int((c.real-MIN)/STEP)] = 1

im.set_data(x-STEP/2, y-STEP/2, z)
ax.images.append(im)

real = []
imag = []

for c in c_numbers:
    real.append(c.real)
    imag.append(c.imag)

ax = axs[0][1]
ax.set_title('Hexbin')
ax.hexbin(real, imag, gridsize=100, cmap='inferno')

ax = axs[1][0]
ax.set_title('Scatter')
ax.scatter(real, imag, s=2)

ax = axs[1][1]
ax.set_title('Hist2d')
ax.hist2d(real, imag, bins=100)

plt.show()