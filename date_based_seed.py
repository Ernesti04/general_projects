import datetime
import math

dt = datetime.datetime.now()
yearA = int(dt.strftime("%Y"))
day = int(dt.strftime("%j"))
seed = ((int(str( math.sqrt( yearA*365.251 + day ) )[-7:] ) * day) // 2) + 1
print(yearA, day, seed, "\n")

yearVals = []
counter = 0
dups = []
for i in range(0, 50):
    year = yearA + i
    for day in range(1, 366):
        while True:
            try:
                seed = year*365.251 + day
                seed = int( str( math.sqrt( seed ) )[ -7: ] )
                seed = ((seed * day) // 2) + 1
                break
            except:
                seed = 111
        if seed not in yearVals:
            print(year, day, "Seed: ", seed)
        else:
            print("------------------------")
            counter += 1
            dups.append([year, day, seed])
        yearVals.append(seed)

print("\n", counter, "duplicate(s):")
for dupe in dups:
    print(dupe[0], dupe[1], dupe[2])