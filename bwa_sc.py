import os
import sys
from subprocess import call 

inp = sys.argv[1]
outp = sys.argv[2]


fastqs = os.listdir(inp)

for f in fastqs:
	try:
		sa = f.split('_')
		if sa[1] == '1.fastq.gz':
			#call('~/bwa/bwa-mem2 mem -t 80 UHGG/uhgg '+inp+f+' '+inp+sa[0]+'_2.fastq.gz > '+outp+sa[0]+'.sam', shell=True )
			call('bwa mem  -t 80 metahit_bwa_index/IGC.fa '+inp+f+' '+inp+sa[0]+'_2.fastq.gz > '+outp+sa[0]+'.sam',shell=True)
	except:
		pass
