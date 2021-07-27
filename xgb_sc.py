import sys
import numpy as np
from scipy import sparse
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

Dfile = sys.argv[1]
orderfile = sys.argv[2]
labelfile = sys.argv[3]
ismutation = sys.argv[4]
trelen= int(sys.argv[5])

D = sparse.load_npz(Dfile)
order = open(orderfile).read().split('\n')
order=order[:-1]
D=D.todense()

idx = np.where(D.sum(axis=0))[1]
D=D[:,idx]

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


dtrain = xgb.DMatrix(D, label=y)
param = {'booster': 'dart',
          'max_depth': 25, 'learning_rate': 0.05,
          'objective': 'binary:logistic', 'silent': True,
          'sample_type': 'uniform',
          'normalize_type': 'tree',
          'rate_drop': 0.04,
          'skip_drop': 0.04}
num_round=trelen

rs = np.random.randint(1000)
res = xgb.cv(param, dtrain, num_round, nfold=5,metrics={'error', 'auc','aucpr'}, seed=rs, callbacks=[xgb.callback.print_evaluation(show_stdv=False)])
fm = res['test-aucpr-mean'].argmax()
auc = res.iloc[fm]['test-auc-mean']
auc_st = res.iloc[fm]['test-auc-std']
acc1 = 1-res.iloc[fm]['test-error-mean']
acc1_st = res.iloc[fm]['test-error-std']
aucpr = res.iloc[fm]['test-aucpr-mean']
aucpr_st = res.iloc[fm]['test-aucpr-std']

######################3
acc2=[]
pr=[]
rec=[]
f1=[]
acc2m=[]
prm=[]
recm=[]
f1m=[]


featdict={}
modsize=[]
for i in range(10):
	rs=np.random.randint(1000)
	X_train, X_test, y_train, y_test = train_test_split(D, y, train_size=0.9, random_state=rs,stratify=y)
	dtrain = xgb.DMatrix(X_train, label=y_train)
	dtest = xgb.DMatrix(X_test, label=y_test)
	xgb_model = xgb.train(param, dtrain, trelen)
	predictions = xgb_model.predict(dtest)
	pre = np.round(predictions)
	CR = classification_report(y_test, pre, digits=3,output_dict=True)
	acc2.append(CR['accuracy'])
	if CR['0']['f1-score']>CR['1']['f1-score']:
		pick='0'
	else:
		pick='1'
	pr.append(CR[pick]['precision'])
	rec.append(CR[pick]['recall'])
	f1.append(CR[pick]['f1-score'])
	feat = xgb_model.get_fscore()
	
	for f in feat:
		if f in featdict:
			featdict[f]+=feat[f]
		else:
			featdict[f]=feat[f]
	
	Dm=D[:,[int(f[1:]) for f in feat]]
	X_train, X_test, y_train, y_test = train_test_split(Dm, y, train_size=0.9, random_state=rs,stratify=y)
	dtrain = xgb.DMatrix(X_train, label=y_train)
	dtest = xgb.DMatrix(X_test, label=y_test)
	xgb_model = xgb.train(param, dtrain, 200)
	predictions = xgb_model.predict(dtest)
	pre = np.round(predictions)
	CR = classification_report(y_test, pre, digits=3,output_dict=True)
	acc2m.append(CR['accuracy'])
	if CR['0']['f1-score']>CR['1']['f1-score']:
		pick='0'
	else:
		pick='1'
	prm.append(CR[pick]['precision'])
	recm.append(CR[pick]['recall'])
	f1m.append(CR[pick]['f1-score'])

acc2=np.array(acc2)
pr=np.array(pr)
rec=np.array(rec)
f1=np.array(f1)
acc2m=np.array(acc2m)
prm=np.array(prm)
recm=np.array(recm)
f1m=np.array(f1m)

fo = open(Dfile+'_performance.txt','w')
fo.write('ACC1: '+str(acc1)+'+'+str(acc1_st)+'\n')
fo.write('ACC2: '+str(acc2.mean())+'+'+str(acc2.std())+'\n')
fo.write('ROC: '+str(auc)+'+'+str(auc_st)+'\n')
fo.write('aucPR: '+str(aucpr)+'+'+str(aucpr_st)+'\n')
fo.write('PR: '+str(pr.mean())+'+'+str(pr.std())+'\n')
fo.write('REC: '+str(rec.mean())+'+'+str(rec.std())+'\n')
fo.write('F1: '+str(f1.mean())+'+'+str(f1.std())+'\n')
fo.write('PRm: '+str(prm.mean())+'+'+str(prm.std())+'\n')
fo.write('RECm: '+str(recm.mean())+'+'+str(recm.std())+'\n')
fo.write('F1m: '+str(f1m.mean())+'+'+str(f1m.std()))
fo.close()


select_feat = [k[0] for k in sorted(featdict.items(), key=lambda x: x[1])[::-1] if k[1]>2]
select_feat = [int(s[1:]) for s in select_feat]
if ismutation=='TRUE':
	mutpos = idx[select_feat]#//4 #PRINT THIS TO FILE
	fm=open(Dfile+'_mutat_pos.txt','w')
	fm.write('\n'.join([str(m) for m in mutpos]))
	fm.close()
else:
	fm=open(Dfile+'_gene_no.txt','w')
	mutpos = idx[select_feat]
	fm.write('\n'.join([str(m) for m in mutpos]))
	fm.close()

























