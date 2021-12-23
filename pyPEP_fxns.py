import mechanicalsoup
import re

def get_MHCII_alleles():

    ### Get all MHCII genes from the site and store in "genes" list
	genes=[]
	#open browser to Rankpep site and get all options
	browser = mechanicalsoup.StatefulBrowser()
	browser.open("http://imed.med.ucm.es/Tools/rankpep.html")
	options=browser.get_current_page().find_all('option')
	for x in options:
		x=x.attrs['value']
		if re.search("HLA_D",x):
			genes.append(x)
		elif re.search("I_",x):
			genes.append(x)
	browser.close()
	return genes



import mechanicalsoup
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

def rankpep_submit(fasta,MHC2_gene,organism,rid,outFolder):
	print("Rankpep_submit function on ", organism, " ", MHC2_gene, rid)
	rid=rid.replace("|","")
	filestr=outFolder+'/'+ organism + "_" + MHC2_gene +"_" + rid +'.csv'

	file=Path(filestr)
	if file.is_file():
		print("ALREADY EXISTS:     "+str(file))
		pass

	else:
		fasta=str(fasta)
        #submit form to rankpep site. html response from site is assigned to resp
		browser = mechanicalsoup.StatefulBrowser()
		browser.open("http://imed.med.ucm.es/Tools/rankpep.html")
		browser.select_form('form[action="/cgi-bin/rankpep_mif.cgi"]')
		browser["MHC"] = '2'
		browser["sequence"] = fasta
		browser['matrixii'] = MHC2_gene
		resp = browser.submit_selected()

        #Parse html with Beautifulsoup
		index=[]
		data=[]

		soup = BeautifulSoup(resp.text,'html.parser')
		table = soup.find_all(width="800")
		table = BeautifulSoup(str(table),'html.parser')
		for num,row in enumerate(table.find_all('tr')):
			info=[]
			color=""
			for x in row.attrs.keys():
					if x == 'bgcolor':
						color=row.attrs['bgcolor']
					if color =="silver":
						color="Color"
					elif len(color) > 3:
						color="RED"
					else:
						color="None"
			if num == 0:
				for pos,col in enumerate(row.find_all('th')):
					index.append(col.text)
				index.append("color")
			else:
				for pos,col in enumerate(row.find_all('td')):
					info.append(col.text)
				info.append(color)

				data.append({
					index[0]:info[0],
					index[1]:info[1],
					index[2]:info[2],
					index[3]:info[3],
					index[4]:info[4],
					index[5]:info[5],
					index[6]:info[6],
					index[7]:info[7],
					index[8]:info[8]
							})
		browser.close()
#Convert data to pandas DataFrame
		df =pd.DataFrame(data)
		if len(df) > 0:
			df=df[['RANK','POS.','N','SEQUENCE','C','MW (Da)','SCORE','% OPT.','color']]

		#save results to csv
			df.to_csv(filestr)
			print(filestr, "CREATED!!")
		else:
			print("no results")
