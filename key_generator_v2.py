import hashlib
import random as rand

def makeHash(hashSeed):
    keyHash = hashlib.new("sha512") 						# set up 512 bit hash (128 hex chars)
    hashSeed = ''.join(str(hashSeed)).encode("utf-8") 		# encode the seed for hashing
    keyHash.update( hashSeed ) 							# hash the seed
    salt = "bingus".encode("utf-8") 						# prepare salt to make hashes more random
    for i in range(31): 									# hash multiple times, makes hash more random
        prevHash = str(keyHash.hexdigest()).encode("utf-8") 	# get the hex string of the current hash value
        keyHash.update( hashSeed + prevHash + salt ) 		# seed + old hash + salt
    keyHash = list(str(keyHash.hexdigest())) 				# make into hex
    #print(''.join(keyHash))
    return keyHash 									# return hash as hex bits

def readHash(pKey, key2):
    keyHash = makeHash(pKey) 						# get the private hash to work with
    key2 = (hex(int(key2, 16) ^ int((''.join(keyHash) + ''.join(keyHash)), 16))[2:]).zfill(256)  # reverse the xor using key and private key
    #print(key2)
    
    # split public key back into groups of 2 hex bytes
    instructions = [] 								# store instructions from public key
    for i in range(0, len(key2), 2): 					# for every other hex byte in public key
        instructions.append(key2[i : i+2]) 				# save it and the nex one
        
    for i in range(len(instructions)): 					# for each instruction
        instructions[i] = int(''.join(instructions[i]), 16) 	# convert to decimal
    #print("instruction positions: ", instructions)
    
    # read each postion and store the character
    key2 = instructions 						# update public key to be indexes
    instructions = [] 						# reset to hold chars at indexes
    for i in range(len(key2)): 				# for each instruction location
        
        if int(key2[i]) > 127: 					# if out of range
            key2[i] -= 128 						# bring back in range
            
        keyVal = keyHash[key2[i]] 				# get the character at that position
        
        if keyVal == "f": 						# check for rehash value
            keyHash = makeHash(keyHash) 		# rehash if found
            continue 							# skip to avoid adding it in
        
        instructions.append(keyVal) 			# save the character that was found
    #print("instructions: ", instructions, "\n")
    
    # interpret the instructions
    prevFlag = "" 							# store previous instruction when not number
    ind = 0 								# store index to save to from a, b, c, d
    abcd = [[], [], [], []] 						# array to hold values
    for i in instructions: 					# go through all instructions
        if i in ["a", "b", "d"]: 					# if instruction instead of number
            # a is change index, b is next index, d is filler character
            prevFlag = i 						# store the value 
            continue 							# go onto the next isntruction
        
        if prevFlag == "a": 					# if the previous instruction was to change index
            prevFlag = "" 						# reset the previous flag as it's been used
            ind = int(i) 						# change the index to match the current value
            continue 							# go to next instruction
        
        if prevFlag == "b": 					# if the previous instruction was to "move on"
            prevFlag = "" 						# reset the previous flag as it's been used
            ind += 1 							# change the index to match the next one
        
        if i == "c": 							# check for c
            i = "-" 							# indicates a negative value
        
        abcd[ind] += i 						# if instruction not a flag, save to current index
        
    #print(abcd)
    for i in range(4): 						# for each final value
        abcd[i] = int(''.join(abcd[i])) 			# format to be used
        
    return abcd[0], abcd[1], abcd[2], abcd[3] 	# return the extracted values
        

def sortChars(seed, arr, chars): 	# get character positions in hash
    tmpSeed = rand.seed() 			# store current random seed to restore after
    rand.seed(seed) 				# prepare shuffling using the private key
    keyPos = [] 					# prepare the array to store the positions for each character
    for char in chars: 				# go through each possible character
        keyPos.append([]) 			# make room for set
        for i in range(len(arr)): 		# go through every char in hash
            if arr[i] == char: 			# if the char matches the current character
                keyPos[-1].append(i) 		# add it to the list
        rand.shuffle(keyPos[-1]) 		# shuffle each set of positions
    rand.seed(tmpSeed) 			# restore seed to ensure private key doesn't interfere with any other random operations
    return keyPos 					# return list of positions for each character

def fetch(arr, keyPos, char, fill):
    #chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    x = arr.index(char) 					# get index for the character's position set
    y = keyPos[x] 						# get set of positions for the character
    z = y.pop() 							# grab the last value from the list
    z += 128 * rand.randint(0, 1) 			# randomly make high or low value (from 128 bit read hash)
    return hex(z)[2:].zfill(2) 				# return the hex value for that index

def genKey(pKey, abcd, fillFreq):
    high = 10 - fillFreq 								# high end of random pickers
    #rand.seed(abcd) 								# use a seed to
    keyHash = makeHash(pKey) 						# get hash from private key to work with
    kl = 0 											# value to measure key length
    for i in range(len(abcd)): 						# go through variables to put in key
        abcd[i] = list(str(abcd[i])) 						# make sure each number is easier to work with
        kl += len(abcd[i]) 								# add the length of the value to key length
    chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    keyPos = sortChars(pKey, keyHash, chars) 			# make array to store key character positions
    
    # store data and instructions into key
    size = 128 - kl 									# target size of the key - min size of the key
    rh = rand.randint(0, high) 							# how many bytes before rehashing
    k2 = [] 										# holds values for the key
    ind = 0 										# holds the index to read from
    
    while max(len(abcd[0]), len(abcd[1]), len(abcd[2]), len(abcd[3])) > 0: # go through all values in abcd
        
        for value in keyPos: 							# check all the values
            if len(value) <= 1: 							# if any are completely used
                rh = 0 									# mark to rehash to avoid using an empty list
                
        #size -= 1 									# mark that a character gets added to the key
        if rh == 0: 									# check if the re-hash counter reached 0
            hb = fetch(chars, keyPos, "f", 0) 				# get the value for f to indicate a re-hash
            k2.append( hb ) 							# add the value to the key
            keyHash = makeHash(keyHash) 				# get new hash based on the old one
            keyPos = sortChars(pKey, keyHash, chars) 		# remap chars with new hash
            rh = rand.randint(0, high) 						# reset the re-hash counter
            size -= 1 									# mark that a character gets added to the key
        
        if rand.randint(1, 3) == 1: 						# if randomly choosen
            hb = fetch(chars, keyPos, "d", 0) 				# grab a d
            k2.append( hb ) 							# add it to the list
            size -= 1 									# mark that a char was added
            #print(hb)
        
        prevInd = ind 								# store the previous index
        ind = rand.randint(0, 3) 						# get new random index
        while len(abcd[ind]) == 0: 						# if empty at that index
            ind = rand.randint(0, 3) 						# try a new index
        cur = abcd[ind].pop(0) 							# get current character at that index
        
        #print(ind, cur, abcd[ind])
        if prevInd != ind: 								# if different to previous index
            if ind - prevInd == 1: 						# special value if one more (move on)
                hb = fetch(chars, keyPos, "b", 0) 			# get position for b
                k2.append( hb ) 							# add b position to list
                size -= 1 								# added one character
            else: 										# for any other difference
                for swap in ["a", str(ind)]: 				# for a (the marker for index change) and the index
                    hb = fetch(chars, keyPos, swap, 0) 		# get the position value
                    k2.append( hb ) 						# add them in
                size -= 2 								# mark that 2 characters get added to the key
        
        if cur == "-": 									# check for negative sign
            hb = fetch(chars, keyPos, "c", 0) 				# add c to represent it
        else: 										# otherwise
            hb = fetch(chars, keyPos, cur, 0) 				# get the hex value position of the current digit
        k2.append( hb ) 								# add the number into the key
        
        rh -= 1 										# lower re-hash counter
                
    #print("\nkey values: ", k2)
    while size > 0: 									# if space left over in key, fill it
        if len(keyPos[13]) <= 1: 						# check if there's 1 or less filler chars 
            if size > 1: 								# if there's only one space left ignore, otherwise
                hb = fetch(chars, keyPos, "f", 0) 			# get the value for f to indicate a re-hash
                k2.append( hb ) 							# add the value to the key
                keyHash = makeHash(keyHash) 			# get new hash based on the old one
                keyPos = sortChars(pKey, keyHash, chars) 	# remap chars with new hash
                size -= 1 								# mark that rehash char was added
                
        hb = fetch(chars, keyPos, "d", 0) 				# find filler char (d)
        k2.append( hb ) 								# add it to the key
        size -= 1 									# mark that a char was added
        
    k2 = ''.join(k2) 									# convert new key into string
    keyHash = ''.join(makeHash(pKey)) 				# turn key hash into string
    keyHash += keyHash 							# Double it to match new key length
    k2 = (hex(int(k2, 16) ^ int(keyHash, 16))[2:]) 		# xor new key with key hash
    return k2 										# return the finished key

# try to keep total length < 60, more error prone the larger it is
a, b, c = 15, 1, 2
d = 8675309
pKey = "Bingus :3"
rVal = 7 # randomness value, 0-9, higher means more frequent filler values added. set to lower if having issues while using longer values for abcd

key2 = genKey(pKey, [a, b, c, d], rVal)
a, b, c, d = readHash(pKey, key2)

print("private key: ", pKey)
print("private hash: ", ''.join(makeHash(pKey)))
print("public key: ", key2)
print("values: ", a, b, c, d)
