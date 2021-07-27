import sys
import numpy as np
from scipy import sparse
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

Dfile_ra = sys.argv[1]
Dfile_snp = sys.argv[2]
orderfile_ra = sys.argv[3]
orderfile_snp = sys.argv[4]
labelfile = sys.argv[5]
trelen= int(sys.argv[6])

D_ra = sparse.load_npz(Dfile_ra)
order_ra = open(orderfile_ra).read().split('\n')
order_ra=order_ra[:-1]
D_ra=D_ra.todense()
idx_ra = np.where(D_ra.sum(axis=0))[1]
D_ra=D_ra[:,idx_ra]

D_snp = sparse.load_npz(Dfile_snp)
order_snp = open(orderfile_snp).read().split('\n')
order_snp=order_snp[:-1]
D_snp=D_snp.todense()
idx_snp = np.where(D_snp.sum(axis=0))[1]
D_snp=D_snp[:,idx_snp]

shuf = [order_snp.index(x) for x in order_ra]
D_snp = D_snp[shuf,:]

L={}
for l in open(labelfile):
	ll=l.strip().split(',')
	L[ll[0]]=ll[1]
target=[]
for o in order_ra:
	if L[o]=='C':
		target.append(0)
	else:
		target.append(1)
y=np.array(target)

param = {'booster': 'dart',
          'max_depth': 25, 'learning_rate': 0.05,
          'objective': 'binary:logistic', 'silent': True,
          'sample_type': 'uniform',
          'normalize_type': 'tree',
          'rate_drop': 0.04,
          'skip_drop': 0.04}

fo = open(Dfile_ra+Dfile_snp.split('_')[-1]+'_joint_performance.csv','w')
fo.write('acc_ra,pr_ra,rec_ra,f1_ra,acc_snp,pr_snp,rec_snp,f1_snp,acc_join,pr_join,rec_join,f1_join,no_ra_feat,no_snp_feat,no_join_feat,perc_ra_in_join\n')

featdict_ra={}
featdict_snp={}

for i in range(10):
	rs=np.random.randint(1000)
	
	X_train, X_test, y_train, y_test = train_test_split(D_ra, y, train_size=0.9, random_state=rs)
	dtrain = xgb.DMatrix(X_train, label=y_train)
	dtest = xgb.DMatrix(X_test, label=y_test)
	xgb_model = xgb.train(param, dtrain, trelen)
	predictions = xgb_model.predict(dtest)
	pre = np.round(predictions)
	CR = classification_report(y_test, pre, digits=3,output_dict=True)
	acc_ra = CR['accuracy']
	if CR['0']['f1-score']>CR['1']['f1-score']:
		pick='0'
	else:
		pick='1'
	pr_ra = CR[pick]['precision']
	rec_ra = CR[pick]['recall']
	f1_ra = CR[pick]['f1-score']
	feat_ra = xgb_model.get_fscore()
	no_ra = len(feat_ra)
	for f in feat_ra:
		if f in featdict_ra:
			featdict_ra[f]+=feat_ra[f]
		else:
			featdict_ra[f]=feat_ra[f]
	
	X_train, X_test, y_train, y_test = train_test_split(D_snp, y, train_size=0.9, random_state=rs)
	dtrain = xgb.DMatrix(X_train, label=y_train)
	dtest = xgb.DMatrix(X_test, label=y_test)
	xgb_model = xgb.train(param, dtrain, trelen)
	predictions = xgb_model.predict(dtest)
	pre = np.round(predictions)
	CR = classification_report(y_test, pre, digits=3,output_dict=True)
	acc_snp = CR['accuracy']
	if CR['0']['f1-score']>CR['1']['f1-score']:
		pick='0'
	else:
		pick='1'
	pr_snp = CR[pick]['precision']
	rec_snp = CR[pick]['recall']
	f1_snp = CR[pick]['f1-score']
	feat_snp = xgb_model.get_fscore()
	no_snp = len(feat_snp)
	for f in feat_snp:
		if f in featdict_snp:
			featdict_snp[f]+=feat_snp[f]
		else:
			featdict_snp[f]=feat_snp[f]
	
	#D_join = np.hstack((D_ra[:,[int(s[1:]) for s in feat_ra]],D_snp[:,[int(s[1:]) for s in feat_snp]]))
	D_join = np.hstack((D_snp[:,[int(s[1:]) for s in feat_snp]] , D_ra[:,[int(s[1:]) for s in feat_ra]]))
	
	X_train, X_test, y_train, y_test = train_test_split(D_join, y, train_size=0.9, random_state=rs)
	dtrain = xgb.DMatrix(X_train, label=y_train)
	dtest = xgb.DMatrix(X_test, label=y_test)
	xgb_model = xgb.train(param, dtrain, trelen*3)
	predictions = xgb_model.predict(dtest)
	pre = np.round(predictions)
	CR = classification_report(y_test, pre, digits=3,output_dict=True)
	acc_join = CR['accuracy']
	if CR['0']['f1-score']>CR['1']['f1-score']:
		pick='0'
	else:
		pick='1'
	pr_join = CR[pick]['precision']
	rec_join = CR[pick]['recall']
	f1_join = CR[pick]['f1-score']
	feat_join = xgb_model.get_fscore()
	no_join=len(feat_join)
	
	joind = np.array([int(s[1:]) for s in feat_join])
	perc_join = sum(joind<no_ra)/len(joind)
	
	fo.write(str(acc_ra)+','+str(pr_ra)+','+str(rec_ra)+','+str(f1_ra)+','+str(acc_snp)+','+str(pr_snp)+','+str(rec_snp)+','+str(f1_snp)+','+str(acc_join)+','+str(pr_join)+','+str(rec_join)+','+str(f1_join)+','+str(no_ra)+','+str(no_snp)+','+str(no_join)+','+str(perc_join)+'\n')

fo.close()

select_feat_ra = [k[0] for k in sorted(featdict_ra.items(), key=lambda x: x[1])[::-1] if k[1]>2]
select_feat_ra = [int(s[1:]) for s in select_feat_ra]
select_feat_snp = [k[0] for k in sorted(featdict_snp.items(), key=lambda x: x[1])[::-1] if k[1]>2]
select_feat_snp = [int(s[1:]) for s in select_feat_snp]

mutpos = idx_ra[select_feat_ra]#//4 #PRINT THIS TO FILE
fm=open(Dfile_ra+Dfile_snp.split('_')[-1]+'_gene_pos.txt','w')
fm.write('\n'.join([str(m) for m in mutpos]))
fm.close()

mutpos = idx_snp[select_feat_snp]#//4 #PRINT THIS TO FILE
fm=open(Dfile_ra+Dfile_snp.split('_')[-1]+'_mutat_pos.txt','w')
fm.write('\n'.join([str(m) for m in mutpos]))
fm.close()











