from pyPEP_results import *
df=rankpep_out_df('/home/phil/CRISPR_Immunogenicity/rankpep_out2/')
df.to_csv('rankpep_results.csv')
