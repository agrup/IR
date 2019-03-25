import sys
sys.path.append("modulos/dictionary.py")
import getopt
from os import listdir
from os.path import isdir
import modulos.dictionary as dictionary
from modulos.tokenizer import tokenizar

def main(argv):
	dirname = ""
	empty = True
	output = "terminos"

	try:
		opts, args= getopt.getopt(argv,"hd:no:")
	except getopt.GetoptError:
		print("pareserIR")
		print(" -d path to source directory <origin>")
		print(" -n without empty words")
		sys.exit(2)

	for opt, arg in opts:
		if opt=='-h':
			print("pareserIR")
			print(" -d path to source directory <origen>")
			print(" -n without empty words")
			print(" -o output file name")
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
	file_count=0

	
	if isdir(dirname):
		files = listdir(dirname)
		outputFile = open(output+".txt",'w')
		for fileI in files:
			file_tokens =[]
			tokens = []
			file_count +=1
			lines = open(dirname+'/'+fileI,'r').readlines()
			tokens.extend(tokenizar(lines)) 
			if not empty:
				vacias = dictionary.get_vacias("extras/vacias.txt")
				tokens = dictionary.sacar_palabras_vacias(tokens,vacias)
			for token in tokens:	
				if(token in word_dic):
					cf,df = word_dic[token]
					if (token in file_tokens):
						word_dic[token] = cf+1, df
					else:
						file_tokens.append(token)
						word_dic[token] = cf+1, df+1
				else:
					word_dic[token]=1,1
					file_tokens.append(token)		


		ordered_keys = sorted(word_dic, key=word_dic.get, reverse=True)
		
		for token in ordered_keys:
			outputFile.write(token +": "+ str(word_dic[token])+"\n") 
		outputFile.close()	

if __name__ == "__main__":
   main(sys.argv[1:])
