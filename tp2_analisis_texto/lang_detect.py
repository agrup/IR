import sys
import getopt
from os import listdir
from os.path import isdir
from modulos.tokenizer import *
import json
import os
import numpy
import time



def get_lengs(jsonfile):
	data = json.load(open(jsonfile))

	return data



def get_unigramas(line):
	unigramas = []
	for leters in line:
		if leters not in (" "):
			unigramas.extend(leters)
	return unigramas

def get_bigrams(line):
	bigrmas =[]
	for leters in line:

		for i in range(0,len(leters)-1):
			bigrm=leters[i]+ leters[i+1]
			bigrmas.append(bigrm)

	
	return bigrmas
		

def unigrams_to_dic (unigrams):
	unigrams_dic ={}
	leng=(len(unigrams))
	for unigram in unigrams:
		
		if unigram in unigrams_dic:
			unigrams_dic[unigram]+=1
		else:
			unigrams_dic[unigram]=1


	for unigram, value in unigrams_dic.items():
		unigrams_dic[unigram]= value/leng

	return unigrams_dic


def normalize(dic):
	new_dic ={}

	for key, value in dic.items():
		# print(key,value)
		for key_ob, value_ob in dic.items():
			if(key not in key_ob):
				for n_grama , count in value_ob.items():
					if (n_grama not in value):
						value[n_grama]=0



	return dic

def lang_detect (list_leng,file_detect):

	coefs=[]

	for leng , unigrams in list_leng.items():
		new_detec=[]
		lang_params=[]
		for n_grama in unigrams:
			if n_grama in file_detect:
				new_detec.append(file_detect[n_grama])
				lang_params.append(unigrams[n_grama])

			else:
				new_detec.append(0)
				lang_params.append(unigrams[n_grama])


		if len(lang_params) == len(new_detec):
			tup = numpy.corrcoef(lang_params,new_detec),leng
			coefs.append(tup)
	max_len_count = 0
	max_leng=""	

	for c,lenguaje in coefs:
		 
		if c[0,1] >= max_len_count:
			max_leng= lenguaje
			max_len_count = c[0,1]

	return(max_leng,max_len_count)



def help():
	print("pareserIR")
	print(" -d path to source directory <origen>")
	print(" -o path to output directory <destination>")
	print(" -u unigrama default")
	print(" -b bigrama ")
	print(" -t train use file name for the lenguaje")



	#print(" -o output file name")

def main(argv):
	dirname = ""
	training = False
	output = "lang/"
	unigrams_flag=True
	testFile="languageIdentificationData/solution"


	unigrams_flag=True
	if len(sys.argv) <= 1:
		help()
		exit()
	try:
		opts, args= getopt.getopt(argv,"hd:ubt")
	except getopt.GetoptError:
		help()
		sys.exit(2)

	for opt, arg in opts:
		if opt=='-h':
			help()
			exit()
		elif opt in ("-d"):
			dirname = str(arg)
		elif opt in ("-t"):
			training = True
		elif opt in ("-b"):
			unigrams_flag=False
			
	
	if not os.path.exists(output):
		os.makedirs(output)

			
#variables usadas
	#list of unigram
	unigrams=[]
	#list of languejes 
	langs=[]
	#dictionary of unigrams

	dics_unigrams={}
	dics_test={}

	if isdir(dirname):

		if (isdir(dirname)):
			files = listdir(dirname)
		else:
			files=[""]
		for file in files:	
			
			unigrams_dic ={}
			langs.append(file)
			if (isdir(dirname)):
				dirictory= os.path.join(dirname,file)
			else:
				dirictory=dirname
			with open(dirictory,'r',errors='ignore') as filer:
				lines = filer.readlines()
				token = tokenizar(lines)
				if(unigrams_flag):
					unigrams.extend(get_unigramas(token))
				else:
					unigrams.extend(get_bigrams(token))
				
				#loop to add unigrams to dictionary
				if(training):

					unigrams_dic = unigrams_to_dic(unigrams)
					
					# tengo que normalizar los diccionarios antes de guardarlo
					
					dics_unigrams[file]=unigrams_dic
					


				else:

					unigrams_dic = unigrams_to_dic(unigrams)
					
					dics_test[file]=(unigrams_dic)

			if not training:
				result=lang_detect(get_lengs(output+"training.json"),unigrams_dic)
				print("lenguaje prediction")
				print(file)
				print(result)


		if (training):
			dics_unigrams=(normalize(dics_unigrams))

			with open(output+"training.json","w") as jsonfile:

				json_dic = json.dumps(dics_unigrams)
				jsonfile.write(json_dic)
			print("json training file successfully created")

	else:
		with open(dirname,'r',errors="ignore") as file:
			lines = file.readlines()
			resultado =[]
			
			for line in lines:
				
				unigrams=[]
				token = tokenizar_l(line)
				if(unigrams_flag):
					unigrams.extend(get_unigramas(token))
				else:
					unigrams.extend(get_bigrams(token))
			

				
				unigrams_dic = unigrams_to_dic(unigrams)
				dics_test[file]=(unigrams_dic)
				jsonlengs=get_lengs(output+"training.json")
				result=lang_detect(jsonlengs,unigrams_dic)
				# print(line)
				resultado.append(result)
				# print(result)
				
			if not(training):
				with open("resultado.txt",'w') as result:
					for r ,v in resultado:
						#print(r)
						result.write(str(r)+"\n")
				
				with open(testFile,'r') as filesolution:
					solutions=[]
					results =[]
					filesol = filesolution.readlines()
					total = len(filesol)
					for line in filesol:
						l = line.split()
						solutions.append(l[1])

					#print(tf.read())
					
					sum_acert=0
					for sol in resultado:
						lengua, count = sol
						
						#print(lengua)
						results.append(lengua)
						#print(resultado)
					
					for i in range(total):
						if(results[i]==solutions[i]):
							sum_acert +=1
					print("acierto")
					print(sum_acert/total)




			




if __name__ == "__main__":
   main(sys.argv[1:])