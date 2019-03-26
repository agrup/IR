import sys
#sys.path.append("modulos/dictionary.py")
import getopt
from os import listdir
from os.path import isdir
import modulos.dictionary as dictionary
from modulos.tokenizer import tokenizar
import collections


def help():
	print("pareserIR")
	print(" -d path to source directory <origen>")
	print(" -n without empty words")
	#print(" -o output file name")


def main(argv):
	dirname = ""
	empty = True
	output = "terminos"
	list_empty="extras/vacias.txt"
	estadistica="estadisticas.txt"



	if len(sys.argv) <= 1:
		help()
		# print("pareserIR")
		# print(" -d path to source directory <origen>")
		# print(" -n without empty words")
		# print(" -o output file name")
		exit()
	try:
		opts, args= getopt.getopt(argv,"hd:no:")
	except getopt.GetoptError:
		help()
		sys.exit(2)

	for opt, arg in opts:
		if opt=='-h':
			help()
			# print("pareserIR")
			# print(" -d path to source directory <origen>")
			# print(" -n without empty words")
			# print(" -o output file name")
			exit()
		elif opt in ("-d"):
			dirname = arg
		elif opt in ("-n"):
			empty = False
		elif opt in("-o"):
			output = arg

	word_count = 0
	word_dic = {}
	vacias = []

	#stadistics
	file_count=0
	tokens_count=0
	terminos_count=0

	max_document_len=0
	max_document_len_terms=0
	max_document_len_tokens=0

	min_document_len=-1
	min_document_len_tokens=0
	min_document_len_terms=0

	len_terms=0
	count_terms__onece=0

	filex=0
	
	if isdir(dirname):
		files = listdir(dirname)
		outputFile = open(output+".txt",'w')
		for fileI in files:
			filex = fileI
			file_tokens =[]
			tokens = []
			file_count +=1
			lines = open(dirname+'/'+fileI,'r',encoding="ISO-8859-1").readlines()
			tokens = tokenizar(lines)

			if not empty:
				vacias = dictionary.get_vacias(list_empty)
				#vacias = dictionary.get_vacias("extras/vacias.txt")
				print("casa")
				tokens = dictionary.sacar_palabras_vacias(tokens,vacias)
			for token in tokens:	
				tokens_count +=1
				
				if(token in word_dic):
					cf,df = word_dic[token]
					if (token in file_tokens):
						word_dic[token] = cf+1, df
					else:
						file_tokens.append(token)
						len_terms += len(token)
						word_dic[token] = cf+1, df+1
				else:
					word_dic[token]=1,1
					file_tokens.append(token)
					len_terms += len(token)



			if len(tokens) < min_document_len or min_document_len == -1:
				min_document_len = len(tokens)
				min_document_len_terms= len(file_tokens)
				min_document_len_tokens=len(tokens)


			if (len(tokens)> max_document_len):
				max_document_len=len(tokens)
				max_document_len_terms = len(file_tokens)
				max_document_len_tokens =len(tokens)

		#print(sorted(word_dic))
		terminos_count = len(word_dic)
		ordered_keys = sorted(word_dic)
		for key in ordered_keys:
			cf,df = word_dic[key]
			outputFile.write(str(key)+"\t"+str(cf)+"\t"+str(df)+"\n")
			if (cf==1):
				count_terms__onece +=1
		outputFile.close()	

		print("numero de docuemtons: "+str(file_count))
		print(str(tokens_count)+" "+str(terminos_count))
		mean_tokens = tokens_count/ file_count
		mean_terms = terminos_count/file_count
		print(str(mean_tokens)+" "+str(mean_terms))
		len_mean_terms = len_terms/terminos_count
		print(len_mean_terms)
		print(str(min_document_len_terms)+"\t"+str(min_document_len_tokens))
		print(str(max_document_len_terms)+"\t"+str(max_document_len_tokens))
		print(count_terms__onece)

		with open(estadistica,"w") as static:
			static.write(str(file_count)+"\t\n")
			static.write(str(tokens_count)+" "+str(terminos_count)+"\t\n")
			static.write(str(mean_tokens)+" "+str(mean_terms)+"\t\n")
			static.write(str(len_mean_terms)+"\t\n")
			static.write(str(min_document_len_terms)+"\t"+str(min_document_len_tokens)+"\t\n")
			static.write(str(max_document_len_terms)+"\t"+str(max_document_len_tokens)+"\t\n")
			static.write(str(count_terms__onece)+"\t\n")
			

if __name__ == "__main__":
   main(sys.argv[1:])

