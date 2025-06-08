import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.patches import Circle
import numpy as np
import math
fig, ax = plt.subplots()
alphabet = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
spacers = [" ", ".", ",", "-", "!", "?"]
dist = 5
w = 0
words = [[]]
puncuation = []
data = []

def askConfig():
    if function != 1:
        while True:
            try:
                split = int(input("Split text by non-alphabet or number characters? 0 for no, 1 for yes: "))
                break
            except:
                split = 0
                break
        while True:
            try:
                obfuscate = int(input("Encrypt circle by shifting points? 0 for no, 1 for yes: "))
                break
            except:
                obfuscate = 0
    else:
        split, obfuscate = 1, 0
    col = input("Points color (css color name): ")
    #col1 = input("Background color: ")
    col2 = input("Line color: ")
    col3 = input("Circle color: ")
    return split, obfuscate, col, col2, col3


def graph():
    print("\nCircle binary data:")
    print(''.join(data))
    #ax.set_facecolor(color1)
    ax.set_aspect('equal')
    plt.grid(False)
    ax.set_axis_off()
    plt.title(''.join(text))
    plt.show()

def encrypt():
    order = []
    tmp = []
    for i in range(size):
        order.append(i)
        tmp.append([])
    np.random.shuffle(order)
    print(f'New order: {order}')
    point = 0
    for i in order :
        tmp[point] = points[i]
        point += 1
    for i in range(size):
        points[i] = tmp[i]
    
def splitText():
    w = 0
    p = 0
    for char in text:
        if char == "\n":
            continue
        if char in spacers:
            if p == 0: 
                ''.join(words[w])
                words.append([])
                puncuation.append(char)
                w += 1
                p += 1
        else:
            words[w].append(char)
            p = 0

def genCons():
    #for con in connections:
        #print(con)
    for k in range(len(connections)):
        cons = connections[k]
        for x in range(len(cons)):
            con = cons[x]
            #print(con)
            if (con == "1"):
                start = 0 - x
                if start < 0:
                    start += size
                end = start + (k + 1)
                if end > (size-1):
                    end -= size
                line = [[points[start][0], points[end][0]], [points[start][1], points[end][1]]]
                #print(line)
                plt.plot(line[0], line[1], lw=1, c=color2)

def genAngles(n):
    step = 360/n
    for i in range(n):
        point = int(round((step / 2) + (step * i), 0))
        points.append(point)
        #print(point)

def genPoints(w):
    for i in range(len(points)):
        angle = math.radians(points[i] + 90)
        point = [round(-1 * dist * math.cos(angle), 5) + (w * (dist * 2 + 2)), round(dist * math.sin(angle), 5)]
        #print(f'Point {points[i]:3d} at x = {point[0]}, {point[1]}')
        points[i] = point

def genPunc(pun):
    pun1 = Circle(((w * (dist * 2 + 2)), 0), radius=.3, edgecolor=color3, facecolor='white')
    pun2 = Circle(((w * (dist * 2 + 2)), 0), radius=.5, edgecolor=color3, facecolor='white')
    x = spacers.index(pun)
    if x>3:
        ax.add_patch(pun2)
    if x==2 or x==3 or x == 6 or x == 7:
        ax.add_patch(pun1)
    if x == 1 or x == 3 or x == 5 or x == 7:
        plt.plot(points[int((len(points)-1)/2)][0], 0, ".", color=color3)

def genCirc(pun):
    circ = Circle(((w * (dist * 2 + 2)), 0), radius=dist+.5, edgecolor=color3, facecolor='white')
    circ1 = Circle(((w * (dist * 2 + 2)), 0), radius=dist+.25, edgecolor=color3, facecolor='white')
    circ2 = Circle((points[0][0], points[0][1]), radius=.2, edgecolor=color2, facecolor='white')
    ax.add_patch(circ)
    ax.add_patch(circ1)
    ax.add_patch(circ2)
    if split == 1:
        genPunc(pun)
    for start in points:
        for end in points:
            bg_lines.append([[start[0], end[0]], [start[1], end[1]]])
    for line in bg_lines:
        plt.plot(line[0], line[1], lw=.5, c=(0.5, 0.5, 0.5, 0.3))
    if (obfuscate == 1):
        encrypt() # shuffles point order around
    for point in points:
        coords[0].append(point[0])
        coords[1].append(point[1])
    x = np.array(coords[0])
    y = np.array(coords[1])
    plt.scatter(x, y, s=None, c=color)
    genCons()

def generate(n): 				# function to generate uniques
    x = 1 						# start at 1, avoid all 0s case
    while (x < 2**n): 			# for each possible number
        if len(uniques) > (len(alphabet) + len(spacers)):
            break
        s = str(bin(x)[2:].zfill(n)) 	# get binary of number
        cycle = [] 				# get blank list to check rotations
        for i in range(len(s)-1): 	# for each bit in the sequence
            #rot = cycle[i][-1] + cycle[i][:-1] #slightly slower
            rot = s[i:] + s[:i] 		# rotate by i bits
            cycle.append(rot) 		# add each rotation
            if rot < s : 				# if rotation found that is smaller
                break 				# stop searching
        if min(cycle) == s : 		# if the number is already minimum
            uniques.append(s) 		# add to the list
            #print(f'\t{s}') # print results (slow)
        x += 2 					# count odds, halves time
    x=0
    #print(f'Alphabet {w}: ')
    for letter in alphabet:
        #print(f'\t{letter}\t{uniques[x]}')
        match.append([letter, uniques[x]])
        x+=1
    if function != 1:
        for spacer in spacers:
            match.append([spacer, uniques[x]])
            x+=1
    else:
        spc = []
        for spacer in spacers:
            spc.append([spacer, uniques[x]])
            x+=1
            for item in spc:
                if puncuation[w] in item:
                    puncuation[w] = item[0]
                    if function != 1:
                        data.append(str(item[1]))
    for item in match:
        for i in range(len(word)):
            if word[i] in item:
                word[i] = item[0]
    if function != 1:
        l = 1
    else:
        l = 0 #
    for i in range(len(word) + l):
        for item in match:
            if i < len(word):
                if word[i] in item:
                    #print(f'{item[0]}\t{item[1]}\tK = {i+1}')
                    if function != 1:
                        data.append(str(item[1]))
                    else:
                        title.append(item[0])
                        word[i] = item[0]
                    tmp = []
                    for j in range(len(item[1])):
                        tmp.append(item[1][-1 - (j)])
                    connections.append(tmp)
                    #print(f'{item[1]} {''.join(tmp)}')
            else:
                if puncuation[w] in item and function != 1:
                    #print(f'{item[0]}\t{item[1]}\tcenter')
                    data.append(str(item[1]))
                    

def genHeader(s):
    # byte 1 for size, byte 2 for char count
    headerInfo = bin(s)[2:].zfill(7)
    headerInfo2 = bin(len(word))[2:].zfill(8)
    header = "1" + str(headerInfo) + headerInfo2
    data.append(header)

def readHeader(b):
    size = ''.join(b[1:8])
    size = int(size, 2)
    width = ''.join(b[8:])
    width = int(width, 2)
    #print(''.join(b), size, width)
    return size, width

def readBin(b):
    cur = 0
    w = 0
    while cur < len(b):
        scale, count = readHeader(b[cur:cur+16])
        cur += 16
        chars = 0
        while cur < len(b):
            if b[cur] == "1":
                break
            else:
                char = []
                for x in range(scale):
                    char.append(b[cur+x])
                if chars < count:
                    words[w].append(''.join(char))
                    chars += 1
                elif chars == count:
                    puncuation.append(''.join(char))
                    chars += 1
                #print(words[w])
                cur += scale
        words.append([])
        w += 1
        

while True:
    try:
        function = int(input("0 for standard mode, 1 for binary input: "))
        break
    except:
        function = 0

if function != 1:
    text = list(input("Word to be generated: "))
    split, obfuscate, color, color2, color3 = askConfig()
    if split == 1:
        splitText()
    else:
        words = [''.join(text)]
        puncuation.append([])
else:
    text = list(input("Binary input: "))
    data = ''.join(text)
    split, obfuscate, color, color2, color3 = askConfig()
    readBin(text)
    title = []
    


fig.set_figwidth(len(words) * (dist * 2 + 2)) 
w = 0
for word in words:
    if word == []:
        continue
    uniques = []
    match = []
    points = []
    coords = [[], []]
    bg_lines = []
    connections = []
    size = max((len(word) * 2 + 3), 11) # ensure second number results in more possibilities than alphabet size
    if len(puncuation) < w+1:
        puncuation.append(" ")
    if function != 1:
        print(f'Text: {"".join(word)}{puncuation[w]}\n\tCircle size: {size}')#\nMax K value: {size//2}')
    if function != 1:
        genHeader(size)
    generate(size)
    genAngles(size)
    genPoints(w)
    genCirc(puncuation[w])
    w += 1


if function == 1:
    for x in range(len(puncuation)):
        words[x].append(puncuation[x])
        if puncuation[x] != ' ':
            words[x].append(' ')
        words[x] = ''.join(words[x])
        #print(words[x])
    text = ''.join(words[:len(puncuation)])
    print(f'Text: {text}')

graph()