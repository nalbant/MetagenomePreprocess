import os
import numpy as np
from scipy import sparse


dataset=['cirrhosis','CC1','wt2d','Liver_Disorder','hypertension','kalp']

S = np.zeros()###################

arrange=################

def snpset(snppos):
	snp={}
	cou=0
	for l in open(snpset):
		ll=l.split('\t')
		snp[ll[0]]=cou
		cou+=1
	return snp

for i,d in enumerate(dataset):
	D_i = sparse.load_npz('/data/'+d+'/SNP/SNP_matrix_filt_0.05.npz')
	m,n=D_i.shape
	SS=np.zeros((m,m))
	snp_i = snpset('/data/'+d+'/SNP/SNP_pos_chi2_0.05.txt')
	for ii in range(m):
		for jj in range(ii+1:m):
			SS[ii,jj] = np.abs(D_i[ii]-D_i[jj]).sum()
	S[arrange[i]:arrange[i+1],arrange[i]:arrange[i+1]]=SS
	for j in ramge(i+1,6):
		snp_j = snpset('/data/'+dataset[j]+'/SNP/SNP_pos_chi2_0.05.txt')
		D_j = sparse.load_npz('/data/'+dataset[j]+'/SNP/SNP_matrix_filt_0.05.npz')
		mm,nn=D_j.shape
		#JOİNT SNP BUL
		# JOİNT OLMAYANI DİFF E EKLE