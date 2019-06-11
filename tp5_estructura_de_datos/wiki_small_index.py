
from structure import *
from modulos.tokenizer import tokenizar
from TAAT import *
from query_parse import *

FORMAT_STRUCT="{}I"
FORMAT_SIZE=4
postin_file="posting_list_wiki.bin"
voc_file="voc_wiki.txt"

dirname="/home/agu/Unlu/IR/colecciones/wiki/en/"


vocs,posting = (indexer(dirname))
save_posting(vocs,posting,postin_file,FORMAT_STRUCT)
# len_data=len(binary_pack([1],FORMAT_STRUCT))
# size = int(os.path.getsize(postin_file)/len_data)   
save_voc(vocs,voc_file)

