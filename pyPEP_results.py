##main create database 
import pandas as pd
import glob
import time

##get all results into one csv with allele vs orgaisms hits count
def rankpep_out_df(folder_name):
    data=[]
    Folder = [] 
    Folder = glob.glob(folder_name+'/*.csv')

    start=time.time()

    for count,file in enumerate(Folder):
        filename=file.split("/")[-1] # remove 'foldername/'
        #print(filename)
        split=filename.split("_")
        
        ##get infor from file_name
        allele=split[2] + "_" + split[3]
        allele=allele.split(".")[0]
        if allele.split("_")[0] != "HLA" or allele.split("_")[0] != "I":
            for xx,ww in enumerate(split):
                if ww == "HLA" or ww == "I":
                    allele=split[xx] + split[xx+1]
        ID=split[-2]
        organism=split[0]+ "_" + split[1] #+"_"+ID
        #print(ID,'\t',organism,'\t',allele,'\n')

        ##get # of red hits from rankpep data file and append to info
        df=pd.read_csv(file)
        redcell=len(df.query('color=="RED"'))

        ## append info to data
        data.append({'Reds':redcell,
                    'Allele': allele,
                    'Organism': organism,
                    'Fasta_ID': ID,
                    })
        if count % 10000 == 0:
            print('Status: ', round(count/len(Folder)*100,2),'%')

    hits=pd.DataFrame(data)
    
    stop=time.time()
    print("Total time: ", stop-start)
    return hits 
