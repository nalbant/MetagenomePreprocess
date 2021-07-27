import sys
import numpy as np
from scipy import sparse

Dfile = sys.argv[1]
abungene = sys.argv[2]
snppos = sys.argv[3]
selectedmuts = sys.argv[4]
selectedmuts+='_mutat_pos.txt'


D = sparse.load_npz(Dfile)
D=D.todense()
print(D.shape)

gen={}
count=0
for g in open(abungene):
	gen[g.strip()]=count
	count+=1
mut=[]
for i in open(selectedmuts):
	mut.append(int(i.strip())//4)
mut=set(mut)

snpgen = []
cou=0
for l in open(snppos):
	ll=l.split('\t')
	if cou in mut:
		snpgen.append(ll[1])
	cou+=1

snpgen=list(set(snpgen))

idx=[]
for s in snpgen:
	idx.append(gen[s])

D=D[:,idx]
print(D.shape)
sparse.save_npz(Dfile, sparse.csr_matrix(D))