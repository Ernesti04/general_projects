import timeit # used to measure time

def generate(): # function to generate uniques
    for x in range(2**n -1): # for each possible number
        s = str(bin(x)[2:].zfill(n)) # get binary of number
        cycle = [] # get blank list to check rotations
        for i in range(len(s)): # for each bit in the sequence
            cycle.append(s[i:] + s[:i]) # add each rotation
        if min(cycle) == s : # if the number is already minimum
            uniques.append(s) # add to the list

time1 = timeit.default_timer() # start timer
uniques = [] # final list
n = 13 # number of bits
generate()
print(f"{len(uniques)} binary necklaces of length {n}:")
time1end = timeit.default_timer() # end timer
print(f'run time: \t{round(time1end - time1, 2)} seconds')

#for unique in uniques: # loop through list
#    print(unique) # print each
