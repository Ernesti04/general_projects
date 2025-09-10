from sympy import isprime as isP
import random
import math
import sys
import os
import key_generator_v2 as keyGen

# private key, change to match what you want
pKey = "Bingus :3"
# encryption variaibles, change to alter behavior
a, b, c = 15, 1, 2
d = 8675309
rVal = 7

# -h message
helpMsg = """Usage:
\tnecklace_encryption.py {-e | -d} [-o output_type] {-f input_file | -t input_text} [-s output_file]
\tnecklace_encryption.py -h
\tnecklace_encryption.py 

Description:
\tA program for encrypting data with binary necklaces as the base mechanism. Run without arguments for an interactive process or with arguments for more configurability. Program written by Ernesti ( github.com/Ernesti04 )

Options:
\t-e \n\t\tSet program to encrypt. Will result in encrypted text as the output.
\t-d \n\t\tSet the program to decrypt an encrypted input.
\t-s \n\t\t
\t-o \n\t\tSet the output type. \n\t\t-b for binary output.  \n\t\t-h for hex output. \n\t\t-c for compressed hex output.
\t-f input_file\n\t\tThe file that text will be taken from from encryption. 
\t-t input_text\n\t\tPlaintext input. Place within quotes to properly encrypt.
\t-s output_file \n\t\tWrites output to file. When output_file matches input_file it will overwrite input_file. 
"""

#alphabet of characters
alphabet  = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
alphabet += ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",]
alphabet += ["@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "\\", "|", "'", '"', "<", ">", "/", "`", "~", ":", ";", "…", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
alphabet += [" ", ".", ",", "!", "?", "\t", "\n"]

def varSetup(args, pKey):
    if len(args) >= 256:
        a, b, c, d = keyGen.readHash(pKey, args[:256]) # argument is the key, reverse to decrypt
    else:
        a, b, c, d, rVal = args # use arguments to generate key and encrypt
    
    casSeed = (101 * max(int(str(a) + str(b) + str(abs(c))), int(d/a))) / min(int(str(a) + str(b) + str(abs(c))), int(d/a)) # cascade initial value
    while casSeed > 9999:			# if too large
        casSeed /= (math.pi * a)		# decrease value
    casSeed = int(casSeed)		# ensure result works with formatting
    
    # checking variables here, don't touch
    if a < 50:
        aRange = ( (1/a) * sum(2**(math.gcd(i,a)) for i in range(1, a+1)) ) / abs(c)
        if len(alphabet) > aRange:
            raise ValueError("Not enough necklace values available. ")
    if isP(a):
        raise ValueError("a is prime, please chose another value.")
    if b > (2**(a - 1)) or b < 1:
        raise ValueError("b value out of range.")
    if (b % 2) == 0:
        raise ValueError("b must be an odd value.")
    random.seed(d) # use alphabet seed
    random.shuffle(alphabet) #shuffle alphabet acording to seed
    random.seed(None) # remove seed so less predictable
    
    if len(args) < 256: # if encrypting, generate the key and return that
        return keyGen.genKey(pKey, [a, b, c, d], rVal), casSeed
    return a, b, c, d, casSeed # return abcd instead if decrypting

def cascade(casSeed, casText): # casText is text to cascade
    newWord = ""
    cs = casSeed
    for l in list(casText):
        new = alphabet.index(l) + cs + casSeed
        while new >= len(alphabet):
            new -= len(alphabet)
        newWord += alphabet[new]
        #print(new, l, alphabet[new])
        cs = new
    #word = list(newWord)
    return newWord
    #print(text, newWord)

def decascade(casSeed, deCasText): # deCasText is text to reverse cascade
    oldWord = ""
    cs = casSeed
    for l in deCasText:
        tmp = alphabet.index(l)
        old = alphabet.index(l) - cs - casSeed
        while old < 0:
            old += len(alphabet)
        oldWord += alphabet[old]
        cs = tmp
    return oldWord

# obfuscate values, make it harder to brute force or analyze without length
def randRot(num): #ensure first bit is not a 1
    i = random.randint(0, len(num)-1)
    rand = num[i:] + num[:i]
    #print(rand)
    return rand

# deobfuscate values, when length is known makes values useable
def minRot(num):
    num = str(num)
    minimum = num
    for i in range(len(num)):
        newMin = num[i:] + num[:i]
        if int(minimum) > int(newMin):
            minimum = newMin
    #print(minimum)
    return minimum

# generate necklaces
def generate(n, text): 									# function to generate uniques
    word = []
    data = ["1"]
    # handle data to be used based on options
    if function == 0: # encode setup
        word = list(cascade(casSeed, text)) # cascade text
    else: # decode setup
        # determine message type and convert to binary if necessary
        if text[0] == "h":
            text = hexToBin(text)
        if text[0] == "x":
            text = decompHex(text)
        data = ''.join(text)
        # read the message binary and convert it into usable data
        readBin(text, word)
    
    uniques = [] 									# stores necklace values
    match = [] 										# holds alphabet matched with necklaces
    x = b 											# start at 1, avoid all 0s case
    while (x < 2**n): 								# for each possible number
        if len(uniques) > len(alphabet): 					# check if enough already gnerated
            break 									# stop if enough already generated
        s = str(bin(x)[2:].zfill(n)) 						# get binary of number
        cycle = [] 									# get blank list to check rotations
        for i in range(len(s)//2 +1): 					# check rotations going both ways
            #rot = cycle[i][-1] + cycle[i][:-1] 				#slightly slower
            rot = s[i:] + s[:i] 							# rotate by i bits
            rotb = s[(len(s) - i):] + s[:(len(s) - i)] 			# reverse rotation, may help find smaller quicker
            cycle.append(rot) 							# add forward rotation
            cycle.append(rotb)							# add reverse rotation
            if rot < s or rotb < s : 						# if rotation found that is smaller
                break 									# stop searching
        if min(cycle) == s : 							# if the number is already minimum
            uniques.append(s) 							# add to the list
            #print(f'\t{s}') 							# print results (slow)
        x += c 										# count odds, halves time
    
    # match each character to a necklace
    x=0
    #print(f'Alphabet: ')
    for letter in alphabet:
        #print(f'\t{letter}\t{uniques[x]}')
        match.append([letter, uniques[x]])
        x+=1
    
    # decrypt, match neclace to letter
    for item in match:
        for i in range(len(word)):
            if word[i] in item:
                word[i] = item[0]
    
    # encrypt, go through text and convert characters to binary from necklace
    if function == 0:
        l = 1
    else:
        l = 0 #
    for i in range(len(word) + l):
        for item in match:
            if i < len(word):
                if word[i] in item:
                    #print(f'{item[0]}\t{item[1]}\tK = {i+1}')
                    if function == 0:
                        data.append(randRot(str(item[1])))
                    else:
                        word[i] = item[0]
    if function == 0:
        data = list(addKey + ''.join(data))
    return data, word

# compress hex data by converting 0s
def compHex(uncomp):
    chars = ["0"]
    chars += ["g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    comp = []
    count = 0
    for i in range(len(uncomp)):
        j = uncomp[-1 - i]
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
            
# converts characters back into 0s
def decompHex(comp):
    chars = ["0"]
    chars += ["g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    decomp = []
    s = str(''.join(comp[1:]))
    for i in range(len(s)):
        j = s[-1 - i]
        if j not in chars:
            decomp.append(j)
        else:
            k = chars.index(j) + 1
            for l in range(k):
                decomp.append("0")
    #print(''.join(decomp))
    decomp = hexToBin(["h"] + decomp)
    return decomp

# convert hex into binary
def hexToBin(s):
    s = str(''.join(s[1:]))
    s = int(s, 16)
    s = bin(s)[2:]
    #print(s)
    return list(s)

# read data to decrypt
def readBin(b, word):
    cur = 1
    w = 0
    while cur < len(b):
        count = (len(b) - cur)//a
        #print(a, count)
        size = a
        chars = 0
        #print(len(b) - cur, a)
        while cur < len(b):
            if len(b) - cur < a:
                return
            char = []
            for x in range(a):
                char.append(b[cur+x])
            word.append(minRot(''.join(char)))
            chars += 1
            #print(words[w])
            cur += a
        w += 1

def readArgs():
    if ("-h" in sys.argv or "-help" in sys.argv): # help message requested
        print(helpMsg)
        sys.exit()
    if (len(sys.argv) < 4): # not enough arguments
        raise ValueError("Too few arguments, please see -h for usage.")
    
    # determine encrypt/decrypt
    if "-e" in sys.argv: # encrypt
        function = 0
    elif "-d" in sys.argv: # decrypt
        function = 1
    else:
        raise ValueError("Must specify encryption or decryption.")
    
    if "-t" in sys.argv:
        text = list(sys.argv[sys.argv.index("-t") + 1])
    elif "-f" in sys.argv:
        with open(sys.argv[sys.argv.index("-f") + 1], "r") as file:
            text = list(file.read())
    else:
        raise ValueError("Must specify input type.")
    
    if "-o" in sys.argv and function == 0: # get output type
        output = sys.argv.index("-o")
        outType = sys.argv[output+1]
        if outType not in ["all", "-h", "h", "hex", "hexadecimal", "-c", "c", "comp", "compressed",  "-b", "b", "bin", "binary"]:
            raise ValueError("Incorrect output type. Must be b (bin), h (hex), c (compressed), or excluded for all.")
    else:
        outType = "all"
        
    if "-s" in sys.argv: # save to file
        outFile = sys.argv[sys.argv.index("-s") + 1]
        if os.path.isfile(outFile):
            confirm = input("Output file already exists, do you wish to overwrite? Type 'yes' to confirm: ")
            if confirm not in ["Yes", "YES", "yes", "Y", "y"]:
                raise ValueError("Must confirm to overwrite file, aborting...")
    else:
        outFile = ""
    
    return function, text, outType, outFile

def userInput():
    # determine if encrypting or decrypting
    while True:
        try:
            function = int(input("0 to encrypt, 1 to decrypt: "))
            break
        except:
            function = 0
    # get text input to encode if not provided in command line
    if function == 0:
        text = list(input("Text input: "))
    else: # if decrypting
        text = list(input("Encoded input: "))
    return function, text

def output(data, word):
    outTxt = "" # output text, results of encryption
    # if decrypting, show decrypted text
    if function == 1:
        if "-s" not in sys.argv: # if not saving to file, format for text
            outTxt += 'Text: '
        outTxt += decascade(casSeed, ''.join(word)) # undo cascade
    # if encoding, display encoded results
    else:
        # add junk data if encoding to deter factoring
        x = random.randint(0, a-1)
        for i in range(x):
            data.append(str(random.randint(0, 1)))
        data = ''.join(data)
        tmp = data[:256]
        data = data[256:]
        hexData = hex(int(data, 2))[2:]
        if len(sys.argv) < 2 and outType != "all":
            outTxt += "\n"
        if outType in ["all", "-b", "b", "bin", "binary"]:
            if outType == "all":
                outTxt += "\nBinary encoded data: " # raw data
            outTxt += tmp + data # raw data
        if outType in ["all", "-h", "h", "hex", "hexadecimal"]:
            if outType == "all":
                outTxt += "\nHex encoded data: " # shortens text by converting to hex
            outTxt += f'{tmp}h{hexData}' # shortens text by converting to hex
        if outType in ["all", "-c", "c", "comp", "compressed"]:
            if outType == "all":
                outTxt += "\nCompressed: " # compress hex on 0s
            outTxt += f'{tmp}x{compHex(hexData)}' # compress hex on 0s
    
    if outFile == "":
        print(outTxt)
    else:
        with open(outFile, "w") as file:
            file.write(outTxt)

# -------------------------------------------------
# ------------------ main ------------------------
# -------------------------------------------------

#print(len(sys.argv), sys.argv)
if len(sys.argv) > 1: # arguments
    function, text, outType, outFile = readArgs()
else: # no arguments
    function, text = userInput()
    outType, outFile = "all", "" # set to a default since interactive mode doesn't include them

if function == 1: # get abcd and cascade seed from input if decrypting
    a, b, c, d, casSeed = varSetup(''.join(text[:256]), pKey) # make sure key is used
    text = text[256:]
else: # make key if encrypting
    addKey, casSeed = varSetup([a, b, c, d, rVal], pKey)

data, word = generate(a, text) # actual encryption/decryption function
output(data, word)
#print(generate(a, text))
