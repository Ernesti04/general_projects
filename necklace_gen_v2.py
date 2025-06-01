import timeit # used to measure times
mode = int(input("Select mode: \n\t0 to generate for N\n\t1 to generate for range 2 to N\nMode: "))
if mode == 1:
    start = 2 # starting N value, change this to limit your generation range
    end = int(input("ending bit length: "))+1 # ending N value, user input
else:
    start = int(input("N = "))
    end = start+1

def generate(): 				# function to generate uniques
    x = 1 						# start at 1, avoid all 0s case
    while (x < 2**n): 			# for each possible number
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

time1 = timeit.default_timer() 	# start timer
for n in range(start, end): 		# loop through bit lengths
    uniques = [] 				# final list
    generate() 				# generate for current N bit length
    print(f"{len(uniques)} binary necklaces of length {n}:")
time1end = timeit.default_timer() # end timer
print(f'run time: \t{round(time1end - time1, 2)} seconds')