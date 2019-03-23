import sys
sys.path.append("modulos/dictionary.py")
import getopt
from os import listdir
from os.path import isdir
import modulos.dictionary as dictionary


def main(argv):
	dirname = ""
	empty = True
	output = "output"

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
	
	if isdir(dirname):
		files = listdir(dirname)
		outputFile = open(output+".txt",'w')
		vacias = dictionary.get_vacias("extras/vacias.txt")
		for fileI in files:
			lines = open(dirname+'/'+fileI,'r').readlines()
			for line in lines:
				words = line.split()
				for word in words:
					if (word not in vacias):	
						word_count+=1
						if(word in word_dic):
							word_dic[word]+=1
						else:
							word_dic.update({word:1})
		outputFile.write("Cantidad de palabras: "+ str(word_count)+"\n")
		outputFile.write("Cantidad de palabras unicas: "+str(len(word_dic.keys()))+"\n")
		outputFile.write("Mas frecuentes:"+"\n")
		ordered_keys = sorted(word_dic, key=word_dic.get, reverse=True)
			
		for i in range(0,5):
			outputFile.write(ordered_keys[i]+": "+ str(word_dic[ordered_keys[i]])+"\n") 
		outputFile.close()	

if __name__ == "__main__":
   main(sys.argv[1:])
