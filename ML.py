import numpy as np
from scipy import sparse
import xgboost as xgb


Dsp = sparse.load_npz('cirrhosis/ABU_filt_chi2_matrix.npz')
order = open('cirrhosis/order_abu_chi2.txt').read().split('\n')

Dsp = sparse.load_npz('cirrhosis/SNP_matrix_filt_0.05.npz')
order = open('cirrhosis/order_0.05.txt').read().split('\n')
order=order[:-1]

D=Dsp.todense()

#############
L={}
for l in open('cirrhosis/label.csv'):
	ll=l.strip().split(',')
	L[ll[0]]=ll[1]
target=[]
for o in order:
	if L[o]=='C':
		target.append(0)
	else:
		target.append(1)
y=np.array(target)
###########################

idx = np.where(D.sum(axis=0))[1]
D=D[:,idx]

##############

dtrain = xgb.DMatrix(D, label=y)
param = {'booster': 'dart',
          'max_depth': 25, 'learning_rate': 0.05,
          'objective': 'binary:logistic', 'silent': True,
          'sample_type': 'uniform',
          'normalize_type': 'tree',
          'rate_drop': 0.04,
          'skip_drop': 0.04}
num_round=50
res = xgb.cv(param, dtrain, num_round, nfold=3,metrics={'error', 'auc','aucpr'}, seed=10, callbacks=[xgb.callback.print_evaluation(show_stdv=False)])

###########################3

import scipy.stats as stats

p=[]
for i in range(D.shape[1]):
	dif=D[:,i].T-y
	su=D[:,i].T+y
	C =[[(su==2).sum(),(dif==-1).sum()],[(dif==1).sum(),(su==0).sum()]]
	oddsratio, pvalue = stats.fisher_exact(C)
	p.append(pvalue)
p=np.array(p)
