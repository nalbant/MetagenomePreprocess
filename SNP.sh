#!/bin/bash
python3 preprocess_scripts/covstat.py /data/$1/cov/ /data/$1/SNP/ /data/metahit_bwa_index/genlen.txt /data/$1/label_bin.csv FALSE $2
python3 preprocess_scripts/vcf2mat.py /data/$1/vcf/ /data/$1/SNP/ /data/metahit_bwa_index/genlen.txt TRUE abundant_gen.txt 0.0 /data/$1/label_bin.csv
python3 preprocess_scripts/xgb_sc.py /data/$1/SNP/SNP_matrix_filt_0.0.npz /data/$1/SNP/order_gen_0.0.txt /data/$1/label_bin.csv TRUE 200
python3 preprocess_scripts/stat_sc.py /data/$1/SNP/SNP_matrix_filt_0.0.npz /data/$1/SNP/order_gen_0.0.txt /data/$1/label_bin.csv
python3 preprocess_scripts/reduce_selected_snp_genes.py /data/$1/SNP/ABU_filt_matrix.npz /data/$1/SNP/abundant_gen.txt /data/$1/SNP/SNP_pos_gen_0.0.txt /data/$1/SNP/SNP_matrix_filt_0.0.npz
python3 preprocess_scripts/xgb_sc.py /data/$1/SNP/ABU_filt_matrix.npz /data/$1/SNP/order_gen_0.0.txt /data/$1/label_bin.csv FALSE 200

python3 preprocess_scripts/covstat.py /data/$1/cov/ /data/$1/SNP/ /data/metahit_bwa_index/genlen.txt /data/$1/label_bin.csv TRUE 1.0
python3 preprocess_scripts/vcf2mat.py /data/$1/vcf/ /data/$1/SNP/ /data/metahit_bwa_index/genlen.txt TRUE abundant_gen_chi2.txt $3 /data/$1/label_bin.csv
python3 preprocess_scripts/xgb_sc.py /data/$1/SNP/SNP_matrix_filt_$3.npz /data/$1/SNP/order_chi2_$3.txt /data/$1/label_bin.csv TRUE 50
python3 preprocess_scripts/stat_sc.py /data/$1/SNP/SNP_matrix_filt_$3.npz /data/$1/SNP/order_chi2_$3.txt /data/$1/label_bin.csv
python3 preprocess_scripts/reduce_selected_snp_genes.py /data/$1/SNP/ABU_filt_chi2_matrix.npz /data/$1/SNP/abundant_gen_chi2.txt /data/$1/SNP/SNP_pos_chi2_$3.txt /data/$1/SNP/SNP_matrix_filt_$3.npz
python3 preprocess_scripts/xgb_sc.py /data/$1/SNP/ABU_filt_chi2_matrix.npz /data/$1/SNP/order_chi2_$3.txt /data/$1/label_bin.csv FALSE 50