import sys
import numpy as np
from scipy import sparse

Dfile = sys.argv[1]
abungene = sys.argv[2]
snppos = sys.argv[3]


D = sparse.load_npz(Dfile)
D=D.todense()
print(D.shape)

gen={}
count=0
for g in open(abungene):
	gen[g.strip()]=count
	count+=1

snpgen = []
for l in open(snppos):
	snpgen.append(l.split('\t')[1])

snpgen=list(set(snpgen))

idx=[]
for s in snpgen:
	idx.append(gen[s])

D=D[:,idx]
print(D.shape)
sparse.save_npz(Dfile, sparse.csr_matrix(D))