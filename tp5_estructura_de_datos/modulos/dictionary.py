from os import listdir
from os.path import isdir


def sacar_palabras_vacias(lista_tokens,lista_vacias):
	# newtokens = []
	# print(lista_vacias)
	# for token in lista_tokens:
	# 	if (token not in lista_vacias):
	# 		newtokens.extend(token)
	# return newtokens
	return[token for token in lista_tokens if token not in lista_vacias]

def get_vacias(lines):
	emptys = []
	for line in lines:
		#line = file.split("\n")
		emptys.extend(line)	
	return emptys


