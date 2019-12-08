from random import randrange
seq = [randrange(10**10) for i in range(100)]
seq.sort()
dd = float('inf')
for i in range(len(seq)-1):
    if seq[i] is seq[i+1]:
        continue
    d = abs(seq[i]-seq[i+1])
    if d < dd:
        x,y,dd = seq[i], seq[i+1], d

print(x, y, dd)