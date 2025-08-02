import random
import math
alphabet  = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
alphabet += ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",]
alphabet += ["@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "\\", "|", "'", '"', "<", ">", "/", "`", "~", ":", ";", "…", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
alphabet += [" ", ".", ",", "!", "?","\t", "\n"]
word = list(str(input("word? ")))
#print(word)
newWord = ""
oldWord = ""

a, b, c = 15, 1, 1
d = 8675309
random.seed(d)
random.shuffle(alphabet) #shuffle alphabet acording to casSeed
random.seed(None)

casSeed = (101 * max(int(str(a) + str(b) + str(c)), int(d/a))) / min(int(str(a) + str(b) + str(c)), int(d/a))
while casSeed > 999:
    casSeed /= (math.pi * a)
casSeed = int(casSeed)

def cascade(casSeed):
    global newWord
    cs = casSeed
    for l in word:
        new = alphabet.index(l) + cs + casSeed
        while new >= len(alphabet):
            new -= len(alphabet)
        newWord += alphabet[new]
        cs = new 

def decascade(casSeed):
    global oldWord
    cs = casSeed
    for l in word:
        tmp = alphabet.index(l)
        old = alphabet.index(l) - cs - casSeed
        while old < 0:
            old += len(alphabet)
        oldWord += alphabet[old]
        cs = tmp

cascade(casSeed)
decascade(casSeed)
#print(casSeed)
print("Cascaded: ", newWord)
print("DeCascaded: ", oldWord)