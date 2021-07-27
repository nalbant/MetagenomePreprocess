import sys
from os import listdir
import numpy as np
from scipy import sparse

inp = sys.argv[1]
out = sys.argv[2]
ref = sys.argv[3]
filt = sys.argv[4]
abb = sys.argv[5]
perc = float(sys.argv[6])
label = sys.argv[7]

################
def samp_filt(label):
	lab=set()
	for l in open(label):
		c = l.strip().split(',')
		lab.add(c[0])
	return lab
################


if filt=='TRUE':
	abugen=set()
	for l in open(out+abb):
		abugen.add(l.strip())

acgt='ACGT'
gene_length={}
SNP={}
for line in open(ref):
	l=line.strip().split('\t')
	ll=l[1][1:-1].split(',')
	gene_length[l[0]]=[int(ll[0]),int(ll[1])]

ref_allel={}


vcff = listdir(inp)
sampfilt = samp_filt(label)
vcff = [c for c in vcff if c.split('_')[0] in sampfilt]
count=0

if filt=='TRUE':
	for f in vcff:
		snp={}
		for line in open(inp+f):
			if line[:5]!='Chrom':
				l=line.split('\t')
				if l[0] in abugen:
					if l[2] in acgt and l[3] in acgt:
						pos= int(l[1]) + gene_length[l[0]][1]
						if pos not in ref_allel:
							ref_allel[pos] = [l[2],1,l[1],l[0]]
						else:
							ref_allel[pos][1]+=1
						snp[pos] = l[3]
		SNP[f.split('_')[0]]=snp
		count+=1
		print(count)
else:
	for f in vcff:
		snp={}
		for line in open(inp+f):
			if line[:5]!='Chrom':
				l=line.split('\t')
				if l[2] in acgt and l[3] in acgt:
					pos= int(l[1]) + gene_length[l[0]][1]
					if pos not in ref_allel:
						ref_allel[pos] = [l[2],1,l[1],l[0]]
					else:
						ref_allel[pos][1]+=1
					snp[pos] = l[3]
		SNP[f.split('_')[0]]=snp
		count+=1
		print(count)

perco= round(perc*len(vcff))

suff=abb.split('.')[0].split('_')[-1]

fo1=open(out+'SNP_pos_'+suff+'_'+str(perc)+'.txt','w')


snp_set = list()
for p in ref_allel:
	if ref_allel[p][1] > perco:
		snp_set.append(p)
		fo1.write(str(p)+'\t'+ref_allel[p][3]+'\t'+ref_allel[p][2]+'\n')
fo1.close()

print('Number of SNPs: '+str(len(snp_set)))

S = np.zeros((len(vcff),len(snp_set)*4), dtype=int)
lookup={'A':0,'C':1,'G':2,'T':3}

fo=open(out+'order_'+suff+'_'+str(perc)+'.txt','w')
for i,s in enumerate(SNP):
	fo.write(s+'\n')
	print('matrix: '+str(i))
	for j,jj in enumerate(snp_set):#SNP[s]:
		if jj in SNP[s]:
			S[i,j*4+lookup[SNP[s][jj]]]=1
		else:
			S[i,j*4+lookup[ref_allel[jj][0]]]=1
fo.close()

if filt=='TRUE':
	sparse.save_npz(out+'SNP_matrix_filt_'+str(perc)+'.npz', sparse.csr_matrix(S))
else:
	sparse.save_npz(out+'SNP_matrix_'+str(perc)+'.npz', sparse.csr_matrix(S))
