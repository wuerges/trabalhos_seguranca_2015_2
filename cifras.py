import argparse
import sys

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-k', type=str, nargs=1,
                           help='The key')
parser.add_argument('-m', type=str, nargs=1,
                           help='The operating mode')
parser.add_argument('-c', type=str, nargs=1,
                           help='The cipher')

args = parser.parse_args()

class Ceasar:
    def parseKey(self, k):
        return int(k)

    def cipher(self, k, t):
        return bytes((c + self.parseKey(k) + 256) % 256 for c in t)

    def decipher(self, k, t):
        return bytes((c - self.parseKey(k) + 256) % 256 for c in t)

class Vigenere:
    def parseKey(self, k):
        kk = list(map(ord, k))
        return kk

    def cipher(self, k, t):
        k1 = self.parseKey(k) * int(1 + len(t) / len(k))
        return self.cipher1(k1, t)

    def cipher1(self, k, t):
        return bytes([(a + b + 256) % 256 for (a, b) in zip(k, t)])

    def decipher(self, k, t):
        k1 = self.parseKey(k) * int(1 + len(t) / len(k))
        return self.cipher1([x * -1 for x in k1], t)


class Transposition:
    def cipher(self, k, t):
        t1 = t + bytes([0] * (int(int(k) - (len(t) % int(k)))))
        return self.cipher1(int(k), t1)

    def cipher1(self, k, t1):
        m = [t1[a:a+k] for a in range(0, len(t1), k)]
        z = zip(*m)
        return bytes([i for sl in z for i in sl])

    def decipher(self, k, t):
        return self.cipher1(int((len(t) + 1) / int(k)), t)

class Substitution:
    def parseKey(self, kf):
        with open(kf, 'rb') as f:
            k = f.read()
        return k

    def cipher(self, k, t):
        return self.cipher1(self.parseKey(k), t)

    def cipher1(self, k, t):
        return bytes([k[ti] for ti in t])

    def decipher(self, k, t):
        ks = self.parseKey(k)
        vs = {}
        for i in range(len(ks)):
            vs[ks[i]] = i
        #vs = [ks[i] for i in range(len(ks))]
        return self.cipher1(vs, t)

cifras = {"ceasar": Ceasar()
         ,"vigenere": Vigenere()
         ,"substitution": Substitution()
         ,"transposition": Transposition() }

t = sys.stdin.buffer.read()
o = None

if args.m[0] == "c":
    o = cifras[args.c[0]].cipher(args.k[0], t)
elif args.m[0] == "d":
    o = cifras[args.c[0]].decipher(args.k[0], t)

sys.stdout.buffer.write(o)
