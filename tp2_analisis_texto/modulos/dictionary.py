from os import listdir
from os.path import isdir


def sacar_palabras_vacias(lista_tokens,lista_vacias):
	# newtokens = []
	# for token in lista_tokens:
	# 	if (token not in lista_vacias):
	# 		newtokens.append(token)
	# return newtokens
	return[token for token in lista_tokens if token not in lista_vacias]

def get_vacias(file):
	emptys = []
	lines = open(file,"r").readline()
	for line in lines:
		words = lines.split(", ")
		for word in words:
			emptys.append(str(word))	
	return emptys


