import sys
import os
import numpy as np
from scipy import sparse
from scipy.stats import mannwhitneyu


Dfile_snp = sys.argv[1]
orderfile_snp = sys.argv[2]
labelfile = sys.argv[3]
snp_selfile = sys.argv[4]
snpgenfile = sys.argv[5]
inp = sys.argv[6]


D_snp = sparse.load_npz(Dfile_snp)
order_snp = open(orderfile_snp).read().split('\n')
order_snp=order_snp[:-1]
D_snp=D_snp.todense()

L={}
for l in open(labelfile):
	ll=l.strip().split(',')
	L[ll[0]]=ll[1]

target=[]
for o in order_snp:
	if L[o]=='C':
		target.append(0)
	else:
		target.append(1)

y=np.array(target)

snpgen=[]
for g in open(snpgenfile):
	snpgen.append(g.split('\t')[1])

snp={}
genes=set()
for s in open(snp_selfile):
	i=int(s.strip())
	snp[i]=snpgen[i//4]
	genes.add(snpgen[i//4])

genelist =list(genes)
gened={g:i for i,g in enumerate(genelist)}

Dabu=np.zeros((D_snp.shape[0],len(genes)))

covorder=[]
count=0
cov = os.listdir(inp)
for f in cov:
	top=0.0
	samp = f[:-8]
	check=f[-8:]
	if check=='_cov.txt':
		print(samp)
		covorder.append(samp)
		for l in open(inp+f):
			ll=l.strip().split('\t')
			top+=float(ll[1])
			if ll[0] in genes:
				Dabu[count,gened[ll[0]]]=ll[1]
		Dabu[count,:]/=top
		count+=1

shuf = [covorder.index(x) for x in order_snp]
Dabu = Dabu[shuf,:]

fo= open(Dfile_snp+'_Utest_snp_abu.csv','w')
fo.write('GENE,SNP,CLASS\n')
for s in snp:
	mut = np.asarray(D_snp[:,s]).flatten()
	abu = Dabu[:,gened[snp[s]]]
	x=abu[mut==0]
	xy=abu[mut==1]
	st,p1 = mannwhitneyu(x,xy)
	x=abu[y==0]
	xy=abu[y==1]
	st,p2 = mannwhitneyu(x,xy)
	fo.write(snp[s]+','+str(p1)+','+str(p2)+'\n')
fo.close()












