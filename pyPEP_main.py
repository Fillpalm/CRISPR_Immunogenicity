# MAIN RUN RANKPEP
from Bio import SeqIO
import time
import numpy as np
from pyPEP_fxns import *

tpo=[]
counter=0
alleles=get_MHCII_alleles()
start=time.time()
fasta=SeqIO.parse("cas9_all.fasta", "fasta")    # modify for input fasta

for record in fasta:
    counter+=1
    #start timer for current fasta
    fasta_start=time.time()
    
    #get variables for the fasta
    desc=record.description.split(" ")
    for num,x in enumerate(desc):                              #organism name
        if x[0:3] == "OS=":
            organism = desc[num][3:] + "_" + desc[num+1]
    if organism[-1]==".":
        organism=organism[:-1]
    file = ">" + record.description +'\n' +str(record.seq)
    
    #per MHC2 allele
    for allele in alleles:
        rankpep_submit(file,allele,organism,record.id,"rankpep_out2")             #Run rankpep_submit function
        
        
    #stop timer for current fasta, calcuate total time for fasta. Update user
    temp_time=time.time()-fasta_start
    tpo.append(temp_time)
    
    print("time for current fasta: ", temp_time, "Fasta processesd:",counter, '\n')
      
fasta.close()

stop=time.time()
print("----- DONE! " + str(counter) + " rankpep analysis ran -----" )
print("average time per fasta: ", np.mean(tpo))
print("total time: ", stop-start)
