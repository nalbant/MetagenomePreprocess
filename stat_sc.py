import sys
import numpy as np
from scipy import sparse
from scipy.stats import chi2_contingency


Dfile = sys.argv[1]
orderfile = sys.argv[2]
labelfile = sys.argv[3]

D = sparse.load_npz(Dfile)
order = open(orderfile).read().split('\n')
order=order[:-1]
D=D.todense()
snpnum=D.shape[1]//4
Dsu=D.sum(axis=0)
idx=np.where((Dsu!=D.shape[0])&(Dsu!=0))[1]
#idx = np.where(D.sum(axis=0))[1]
D=D[:,idx]
print('Final SNP no: '+str(len(idx)))
L={}
for l in open(labelfile):
	ll=l.strip().split(',')
	L[ll[0]]=ll[1]
target=[]
for o in order:
	if L[o]=='C':
		target.append(0)
	else:
		target.append(1)
y=np.array(target)

p=[]
for i in range(D.shape[1]):
	if i%500000==0:
		print(i)
	dif=D[:,i].T-y
	su=D[:,i].T+y
	C =[[(su==2).sum(),(dif==-1).sum()],[(dif==1).sum(),(su==0).sum()]]
	p.append(chi2_contingency(C)[1])
p=np.array(p)

bonferroni = 0.05/snpnum
fo=open(Dfile+'_bonferroni.csv','w')
for i,pp in enumerate(p):
	if pp < bonferroni:
		fo.write(str(idx[i])+'\t'+str(pp)+'\n')
fo.close()

fo=open(Dfile+'_BH.csv','w')
srtind=np.argsort(p)
for i,pp in enumerate(p):
	if i*0.05/snpnum > p[srtind[i]]:
		fo.write(str(srtind[i])+'\t'+str(p[srtind[i]])+'\n')
fo.close()