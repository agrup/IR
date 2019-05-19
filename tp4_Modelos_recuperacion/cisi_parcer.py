import sys
import os
from os.path import isdir

#dircisi = "/home/agu/Unlu/IR/colecciones/cisi/"
corpus="CISI.ALL"
corpus_result="CISI.ALL.txt"
doc_delimmiter=".W\n"
terrir_open_doc="<doc>\n"
terrir_close_doc="</doc>\n"
cisi_newdocument_delimiter=".X\n"
terrier_open_Id_document='<docno>'
terrier_close_Id_document='</docno>\n'

def parse_corpus(dircisi):
    try:

        with open(dircisi+corpus,'r',encoding='utf-8', errors='ignore') as file_cisi:
            lines= file_cisi.readlines()
            id=1
            i=0
            #print(lines)
            while i <len(lines):
                #pass line in lines:
                #print("casa",len(lines),i)
                if lines[i] in doc_delimmiter:
                    i+=1
                    #print(lines[i],len(lines),i)
                    with open(corpus_result,'a',encoding='utf-8') as cisi_terrier:
                        cisi_terrier.write(terrir_open_doc)
                        cisi_terrier.write(terrier_open_Id_document+str(id)+terrier_close_Id_document)
                        while i < len(lines) and lines[i] != cisi_newdocument_delimiter:
                            cisi_terrier.write(lines[i])
                            i += 1
                        cisi_terrier.write(terrir_close_doc)
                        if lines[i] == cisi_newdocument_delimiter:
                            id+= 1                            
                i+=1
    except IOError as e:
        print (e)

if __name__ == '__main__':
	if len(sys.argv) == 2:
        # path = os.path.normpath(sys.argv[1])
        # path = path.split(os.sep)
		# if not os.path.exists('cisi_corpus'):
		# 	os.mkdir('cisi_corpus')
		parse_corpus(sys.argv[1])
	else:
		print('Invalid params.\n\tUse: python '+sys.argv[0]+ ' name_file.ALL')