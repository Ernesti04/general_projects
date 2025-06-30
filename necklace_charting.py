import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
k = 2
low = int(input("Start = "))
n = int(input("End = "))

def generate(): 				# function to generate uniques
    w = 1
    x = 1 						# start at 1, avoid all 0s case
    while (x < 2**a - 1): 			# for each possible number
        s = str(bin(x)[2:].zfill(a)) 	# get binary of number
        cycle = [] 				# get blank list to check rotations
        for i in range(len(s)-1): 	# for each bit in the sequence
            rot = s[i:] + s[:i] 		# rotate by i bits
            cycle.append(rot) 		# add each rotation
            if rot < s : 				# if rotation found that is smaller
                break 				# stop searching
        if min(cycle) == s : 		# if the number is already minimum
            uniques.append(s) 		# add to the list
            points.append([w, int(s,2 )])
            w += 1
        x += 2 					# count odds, halves time

fig, ax = plt.subplots(1, (n-low+1))
a = 0
coords = []
data = []
for i in range(low, n+1):
    a = i
    #necklaceCount = (1/a) * sum(k**(math.gcd(i,a)) for i in range(1, a+1)) # a replaces n here
    uniques = [] 
    points = []
    generate()
    #print(a, len(uniques), int(necklaceCount))
    coords.append([[], []])
    for point in points:
        coords[a-low][0].append(point[0])
        coords[a-low][1].append(point[1])
    x = np.array(coords[a-low][0])
    y = np.array(coords[a-low][1])
    data.append([x, y])

c = 0
m = len(data)
for i in data:
    ax[c].set_ylim(0, 2**(n-1)) # ignoring all 1s case, next will be 0{n1s}, or half (n-1)
    ax[c].scatter(i[0], i[1])
    ax[c].set_title(f'{c+low}')
    ax[c].set_autoscaley_on(False)
    c+=1

plt.grid(False)
#plt.title(f'Necklace distribution from length 2 to {n}')
plt.show()
