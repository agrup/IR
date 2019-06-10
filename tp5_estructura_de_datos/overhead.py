
from structure import *

###main
FORMAT_STRUCT="{}I"
FORMAT_SIZE=4

dirname="/home/agu/Unlu/IR/colecciones/RI-tknz-data"
vocs,posting = (indexer(dirname))
save_posting(vocs,posting,"posting_list.bin",FORMAT_STRUCT)
len_data=len(binary_pack([1],FORMAT_STRUCT))
size = int(os.path.getsize("posting_list.bin")/len_data)   
save_voc(vocs,"voc.txt")


with open("posting_list.bin","rb") as index:
    size_obj_index=sys.getsizeof(index)
    tuple_index =binary_unpack(index,FORMAT_STRUCT.format(size))
    tuple_array = np.array(tuple_index)
    terms=[]
    for term, value,pt in vocs:
        index.seek(pt)
        docus=index.read(value*len_data)
        postin=struct.unpack(FORMAT_STRUCT.format(value),docus)

# print(os.path.getsize(dirname))

print("directory size",os.path.getsize(dirname))
print("directory posting",os.path.getsize("posting_list.bin"))
print("directory index",os.path.getsize("voc.txt"))
print("---------------------------------------------")
print("overhead",((os.path.getsize("posting_list.bin")-os.path.getsize("voc.txt")-os.path.getsize(dirname))/os.path.getsize("posting_list.bin"))/os.path.getsize("posting_list.bin"),"%")
#print("result",size_obj_index+sys.getsizeof(vocs)-os.path.getsize(dirname))
#print(vocs)


vocs.sort(key=operator.itemgetter(1))
distribution={}
befor_df=vocs[0][1]
aux=0
#print(befor_df)
for _,df,_ in vocs:
    if befor_df==df:
        aux+=1
    else:
        distribution[befor_df]=aux
        aux=1
        befor_df=df
#print(distribution)
# print(vocs)

plot_bar(distribution.values(),distribution.keys())