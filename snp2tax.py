import sys

inp = sys.argv[1]
snppos= sys.argv[2]
outp = sys.argv[3]
ref = sys.argv[4]


tax={}

for l in open(ref):
	ll=l.strip().split('\t')
	tax[ll[1]]=ll[-1]

snp=set()
for l in open(inp):
	ll=l.strip()
	snp.add(int(ll)//4)

i=0
phylo={}
for l in open(snppos):
	if i in snp:
		ind = l.strip().split('\t')[1]
		if tax[ind] not in phylo:
			phylo[tax[ind]]=1
		else:
			phylo[tax[ind]]+=1
	i+=1

fo=open(outp,'w')
fo.write('TAX,COUNT\n')

for p in phylo:
	fo.write(p+','+str(phylo[p])+'\n')
fo.close()