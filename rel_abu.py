import sys
from os import listdir
import numpy as np
from scipy import sparse

inp = sys.argv[1]
out = sys.argv[2]
ref = sys.argv[3]
label = sys.argv[4]
per = float(sys.argv[5])



def samp_filt(label):
	lab=set()
	for l in open(label):
		c = l.strip().split(',')
		lab.add(c[0])
	return lab

#gene lenght
gene={}
for l in open(ref):
	ll=l.split('\t')
	gene[ll[0]] = float(ll[1].split(',')[0][1:])


sampfilt = samp_filt(label)


cov = listdir(inp)
cov = [c for c in cov if c.split('_cov')[0] in sampfilt]

abu={}
mapnum={}
for f in cov:
	top=0.0
	samp = f[:-8]
	check=f[-8:]
	if check=='_cov.txt':
		print(samp)
		for l in open(inp+f):
			ll=l.strip().split('\t')
			top+=float(ll[1])
			if ll[0] not in abu:
				abu[ll[0]]=1.0
			else:
				abu[ll[0]]+=1.0
		mapnum[samp]=top

abugens=set()
thre=len(cov)*per
for a in abu:
	if abu[a] > thre:
		abugens.add(a)
abugen=list(abugens)
fo=open(out+'rel_abu_gen.txt','w')
for a in abugen[:-1]:
	fo.write(a+'\n')
fo.write(abugen[-1])
fo.close()

####
S = np.zeros((len(cov),len(abugen)), dtype=float)
fo2=open(out+'order_rel_abu.txt','w')
coun=0
for f in cov:
	D = {}
	samp = f[:-8]
	check=f[-8:]
	if check=='_cov.txt':
		print(samp+'_2nd')
		fo2.write(samp+'\n')
		for l in open(inp+f):
			ll=l.strip().split('\t')
			if ll[0] in abugens:
				D[ll[0]] = 100*float(ll[1])/gene[ll[0]]/mapnum[samp]
		for i,a in enumerate(abugen):
			if a in D:
				S[coun,i]=D[a]
		coun+=1

fo2.close()
print('COV MATRİX: '+str(S.shape))

sparse.save_npz(out+'rel_abu_matrix_'+str(per)+'.npz', sparse.csr_matrix(S))






