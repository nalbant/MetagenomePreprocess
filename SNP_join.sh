#!/bin/bash
python3 preprocess_scripts/covstat.py /data/$1/cov/ /data/$1/SNP/ /data/metahit_bwa_index/genlen.txt /data/$1/label_bin.csv FALSE $2
python3 preprocess_scripts/vcf2mat.py /data/$1/vcf/ /data/$1/SNP/ /data/metahit_bwa_index/genlen.txt TRUE abundant_gen.txt 0.1 /data/$1/label_bin.csv
python3 preprocess_scripts/xgb_sc.py /data/$1/SNP/SNP_matrix_filt_0.1.npz /data/$1/SNP/order_gen_0.1.txt /data/$1/label_bin.csv TRUE 50