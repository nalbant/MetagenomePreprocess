import sys
from os import listdir
import numpy as np
from scipy import sparse
from scipy.stats import chi2_contingency

inp = sys.argv[1]
out = sys.argv[2]
ref = sys.argv[3]
label = sys.argv[4]
chi2 = sys.argv[5]
per = sys.argv[6]

####
def classdist(label,per):
	cl={}
	lab={}
	for l in open(label):
		c = l.strip().split(',')
		lab[c[0]]=c[1]
		if c[1] in cl:
			cl[c[1]]+=float(per)
		else:
			cl[c[1]]=float(per)
	return cl,lab
###
def find_abugens(defdic,abu,cl):
	abugens=set()
	cc = list(defdic.keys())
	clanum=len(cc)
	for a in abu:
		flag=0
		for i in range(clanum):
			if abu[a][cc[i]]<cl[cc[i]]:
				flag=1
		if flag==0:
			abugens.add(a)
	abugen=list(abugens)
	fo=open(out+'abundant_gen.txt','w')
	for a in abugen[:-1]:
		fo.write(a+'\n')
	fo.write(abugen[-1])
	fo.close()
	return abugen,abugens
###
def find_abugens_chi2(defdic,abu,cl):
	abugens=set()
	cc = list(defdic.keys())
	clanum=len(cc)
	con_tb=np.zeros((2,clanum))
	for a in abu:
		for i,key in enumerate(cc):
			con_tb[0,i] = abu[a][key]
			con_tb[1,i] = cl[key]-abu[a][key]
		if con_tb[1].sum()==0:
			abugens.add(a)
		elif chi2_contingency(con_tb)[1]>0.05:
			abugens.add(a)
	abugen=list(abugens)
	fo=open(out+'abundant_gen_chi2.txt','w')
	for a in abugen[:-1]:
		fo.write(a+'\n')
	fo.write(abugen[-1])
	fo.close()
	return abugen,abugens
###







#gene lenght
gene={}
for l in open(ref):
	ll=l.split('\t')
	gene[ll[0]] = float(ll[1].split(',')[0][1:])

#how many classes to find abundant genes
if chi2=='TRUE':
	cl,lab=classdist(label,1.0)
else:
	cl,lab=classdist(label,per)
defdic={key:0 for key in cl}

cov = listdir(inp)
sampfilt=set(lab.keys())
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
			if float(ll[1])/gene[ll[0]]>=0.1:
				if ll[0] not in abu:
					abu[ll[0]]=defdic.copy()
				abu[ll[0]][lab[samp]]+=1
		mapnum[samp]=top

if chi2=='TRUE':
	abugen,abugens = find_abugens_chi2(defdic,abu,cl)
else:
	abugen,abugens = find_abugens(defdic,abu,cl)

####
S = np.zeros((len(mapnum),len(abugen)), dtype=float)

if chi2=='TRUE':
	fo2=open(out+'order_abu_chi2.txt','w')
else:
	fo2=open(out+'order_abu.txt','w')
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
if chi2=='TRUE':
	sparse.save_npz(out+'ABU_filt_chi2_matrix.npz', sparse.csr_matrix(S))
else:
	sparse.save_npz(out+'ABU_filt_matrix.npz', sparse.csr_matrix(S))





