import numpy as np

alphabet  = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
alphabet += ["@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "\\", "|", "'", '"', "<", ">", "/", "`", "~", ":", ";", "…", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
spacers = [" ", ".", ",", "!", "?"]
w = 0
words = [[]]
puncuation = []
data = []
  
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

def generate(n): 				# function to generate uniques
    x = 1 						# start at 1, avoid all 0s case
    while (x < 2**n): 			# for each possible number
        if len(uniques) > (len(alphabet) + len(spacers)):
            break
        s = str(bin(x)[2:].zfill(n)) 	# get binary of number
        cycle = [] 				# get blank list to check rotations
        for i in range(len(s)//2 +1): 	# for each bit in the sequence
            #rot = cycle[i][-1] + cycle[i][:-1] #slightly slower
            rot = s[i:] + s[:i] 		# rotate by i bits
            rotb = s[(len(s) - i):] + s[:(len(s) - i)]
            cycle.append(rot) 		# add each rotation
            cycle.append(rotb)
            if rot < s or rotb < s : 				# if rotation found that is smaller
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
                        data.append(randRot(str(item[1])))
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
                        data.append(randRot(str(item[1])))
                    else:
                        word[i] = item[0]
                    tmp = []
                    for j in range(len(item[1])):
                        tmp.append(item[1][-1 - (j)])
                    connections.append(tmp)
                    #print(f'{item[1]} {''.join(tmp)}')
            else:
                if puncuation[w] in item and function != 1:
                    #print(f'{item[0]}\t{item[1]}\tcenter')
                    data.append(randRot(str(item[1])))
                    

def randRot(num): #ensure first bit is not a 1
    rand = num
    while(True):
        i = np.random.randint(0, len(num))
        rand = num[i:] + num[:i]
        if rand[0] != "1":
            break
    #print(rand)
    return rand

def minRot(num):
    num = str(num)
    minimum = num
    for i in range(len(num)):
        newMin = num[i:] + num[:i]
        if int(minimum) > int(newMin):
            minimum = newMin
    #print(minimum)
    return minimum

def compress(uncompressed):
    a = 0
    b = 0
    comp = []
    aa = alphabet[-10:] # 1-0
    bb = alphabet[:52] # A-Z a-z
    s = str(uncompressed)
    for i in range(len(s)):
        if s[i] == "1": # if a one
            if b > 0: # if found before compressing 0s
                comp.append(bb[b - 1])
                if b == 1: # 01
                    a -= 1
                b = 0
            a += 1
            if a == len(aa) - 1:
                comp.append(aa[a])
                a = 0
        else: # if a 0
            if a > 0: # if found before compressing 1s
                comp.append(aa[a - 1])
                if a == 1: # 10
                    b -= 1
                a = 0
            b += 1
            if b == len(bb) - 1: 
                comp.append(bb[b])
                b = 0
        if i == len(s) - 1:
            if a > 0:
                comp.append(str(a))
            if b > 0:
                comp.append(bb[b - 1])
    
    return ''.join(comp)
    
def decompress(compressed):
    aa = alphabet[-10:] # 1-0
    bb = alphabet[:52] # A-Z a-z
    s = str(''.join(compressed[1:]))
    decomp = []
    for i in range(len(s)):
        if s[i] == "1":
            decomp.append("1")
            decomp.append("0")
        elif s[i] == "A":
            decomp.append("0")
            decomp.append("1")
        elif s[i] in aa:
            a = aa.index(s[i]) + 1
            for j in range(a):
                decomp.append("1")
        else: # if a 0
            b = bb.index(s[i]) + 1
            for j in range(b):
                decomp.append("0")
    return list(decomp) #''.join(decomp)

def compHex(uncomp):
    chars = ["0"]
    chars += alphabet[:26]
    comp = []
    count = 0
    for i in range(len(uncomp)):
        j = uncomp[i]
        if j == "0":
            count += 1
        else:
            if count > 0:
                k = chars[count-1]
                comp.append(k)
                count = 0
            comp.append(j)
        if i == len(uncomp) - 1 and count > 1:
            comp.append(chars[count-1])
        if count == len(chars):
            comp.append(chars[count - 1])
            count = 0
    return ''.join(comp)
            

def decompHex(comp):
    chars = ["0"]
    chars += alphabet[:26]
    decomp = []
    s = str(''.join(comp[1:]))
    for i in range(len(s)):
        j = s[i]
        if j not in chars:
            decomp.append(j)
        else:
            k = chars.index(j) + 1
            for l in range(k):
                decomp.append("0")
    #print(''.join(decomp))
    decomp = hexToBin(["h"] + decomp)
    return decomp


def hexToBin(s):
    s = str(''.join(s[1:]))
    s = int(s, 16)
    s = bin(s)[2:]
    return list(s)

def genHeader(s):
    # byte 1 for size, byte 2 for char count
    headerInfo = bin(s)[2:].zfill(31) # 32 bytes, 4 bits
    headerInfo2 = bin(len(word))[2:].zfill(16) # 16 bits, 2 bytes
    headerInfo3 = "00000000" + "00000000" # 2 bytes, unused
    header = "1" + str(headerInfo) + headerInfo2 + headerInfo3
    data.append(header)
    #print(header)

def readHeader(b):
    size = ''.join(b[1:32])
    size = int(size, 2)
    width = ''.join(b[32:48])
    width = int(width, 2)
    extra = ''.join(b[48:])
    #print(''.join(b), size, width, extra)
    return size, width

def readBin(b):
    cur = 0
    w = 0
    hs = 64 # header size
    while cur < len(b):
        if (len(b) - cur) < hs - 1:
            break
        scale, count = readHeader(b[cur:cur+hs])
        cur += hs
        chars = 0
        #print(len(b) - cur, scale)
        while cur < len(b):
            if b[cur] == "1":
                break
            else:
                if scale < hs and len(b) - cur < scale:
                    return
                char = []
                for x in range(scale):
                    char.append(b[cur+x])
                if chars < count:
                    words[w].append(minRot(''.join(char)))
                    chars += 1
                elif chars == count:
                    puncuation.append(minRot(''.join(char)))
                    chars += 1
                #print(words[w])
                cur += scale
        words.append([])
        w += 1
        

while True:
    try:
        function = int(input("0 for text input, 1 for binary, hex, or compressed input: "))
        break
    except:
        function = 0

if function != 1:
    text = list(input("Text input: "))
    splitText()
else:
    text = list(input("Encoded input: "))
    if text[0] == "h":
        text = hexToBin(text)
    if text[0] == "c":
        text = decompress(text)
    if text[0] == "x":
        text = decompHex(text)
    data = ''.join(text)
    readBin(text)

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
    #if doGraph != 1:
        #size = 13
    if len(puncuation) < w+1:
        puncuation.append(" ")
    if function != 1 and len(words) < 20:
        print(f'Text: {"".join(word)}{puncuation[w]}\n\tCircle size: {size}')#\nMax K value: {size//2}')
    if function != 1:
        genHeader(size)
    generate(size)
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

data = ''.join(data)
hexData = hex(int(data, 2))[2:]
print(f'\nCircle binary data:\n{data}') # raw data
print(f'\nHex encoded data:\nh{hexData}') # shortens text by converting to hex
print(f'\nCompressed binary: \nc{compress(data)}') # shortens text, focusing on compressing 0s
print(f'\nCompressed hex: \nx{compHex(hexData)}') # compress hex similar to binary, only do 0s
