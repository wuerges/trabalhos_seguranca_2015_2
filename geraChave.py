from random import randint
import sys

#print(randint(0,9))

ks = list(range(256))
vs = []


while ks:
    k = ks.pop(randint(0,len(ks) - 1))
    vs.append(k)

#sys.stdout.buffer.write(bytes(ks))
sys.stdout.buffer.write(bytes(vs))
