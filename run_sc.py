import os
import sys

XXXX=sys.argv[1]

python3 preprocess_scripts/covstat.py /data/XXXX/cov/ /data/XXXX/SNP/ /data/metahit_bwa_index/genlen.txt /data/XXXX/label_bin.csv FALSE 0.85
python3 preprocess_scripts/vcf2mat.py /data/XXXX/vcf/ /data/XXXX/SNP/ /data/metahit_bwa_index/genlen.txt TRUE abundant_gen.txt 0.0
#python3 preprocess_scripts/reduce_snp_genes.py /data/XXXX/SNP/ABU_filt_matrix.npz /data/XXXX/SNP/abundant_gen.txt /data/XXXX/SNP/SNP_pos_gen_0.0.txt
#python3 preprocess_scripts/xgb_sc.py /data/XXXX/SNP/ABU_filt_matrix.npz /data/XXXX/SNP/order_gen_0.0.txt /data/XXXX/label_bin.csv FALSE
python3 preprocess_scripts/xgb_sc.py /data/XXXX/SNP/SNP_matrix_filt_0.0.npz /data/XXXX/SNP/order_gen_0.0.txt /data/XXXX/label_bin.csv TRUE
python3 preprocess_scripts/stat_sc.py /data/XXXX/SNP/SNP_matrix_filt_0.0.npz /data/XXXX/SNP/order_gen_0.0.txt /data/XXXX/label_bin.csv
python3 preprocess_scripts/reduce_selected_snp_genes.py /data/XXXX/SNP/ABU_filt_matrix.npz /data/XXXX/SNP/abundant_gen.txt /data/XXXX/SNP/SNP_pos_gen_0.0.txt
python3 preprocess_scripts/xgb_sc.py /data/XXXX/SNP/ABU_filt_matrix.npz /data/XXXX/SNP/order_gen_0.0.txt /data/XXXX/label_bin.csv FALSE





python3 preprocess_scripts/covstat.py /data/XXXX/cov/ /data/XXXX/SNP/ /data/metahit_bwa_index/genlen.txt /data/XXXX/label_bin.csv TRUE 1.0
python3 preprocess_scripts/vcf2mat.py /data/XXXX/vcf/ /data/XXXX/SNP/ /data/metahit_bwa_index/genlen.txt TRUE abundant_gen_chi2.txt 0.0
python3 preprocess_scripts/reduce_snp_genes.py /data/XXXX/SNP/ABU_filt_chi2_matrix.np /data/XXXX/SNP/abundant_gen_chi2.txt /data/XXXX/SNP/SNP_pos_chi2_0.0.txt
python3 preprocess_scripts/xgb_sc.py /data/XXXX/SNP/ABU_filt_chi2_matrix.npz /data/XXXX/SNP/order_chi2_0.0.txt /data/XXXX/label_bin.csv FALSE
python3 preprocess_scripts/xgb_sc.py /data/XXXX/SNP/SNP_matrix_filt_0.0.npz /data/XXXX/SNP/order_chi2_0.0.txt /data/XXXX/label_bin.csv TRUE
python3 preprocess_scripts/stat_sc.py /data/XXXX/SNP/SNP_matrix_filt_0.0.npz /data/XXXX/SNP/order_chi2_0.0.txt /data/XXXX/label_bin.csv