import struct
from os import listdir
import os
from modulos.tokenizer import tokenizar
import math
import itertools
import numpy as np
import sys
import matplotlib.pyplot as plt
import operator
from typing import List
from os.path import isdir
import time

FORMAT_STRUCT="{}I"
FORMAT_SIZE=4
posting_file="posting_temp.bin"
voc_file="voc_temp.txt"


def get_files(path):

    if not isdir(path):
        return [path]  # its expected to return a list each time even if its a single element
    return [file for fileOrDir in listdir(path) for file in get_files(path + '/' + fileOrDir)]
    # return list of each file returned by the recursive call getFiles(fileOrDir) on
    # each fileOrDir in listdir(path)



def binary_pack(list,FORMAT_STRUCT):
    s_format=FORMAT_STRUCT.format(len(list))
    return (struct.pack(s_format,*list))
    
def binary_unpack(file,s_format):
    content = file.read()
    
    unpackage_data = struct.unpack(s_format,content)
    return unpackage_data

def calc_idf(corpus_count,doc_freq):
    if(doc_freq !=0):
        return math.log(corpus_count/doc_freq,2)
    return 0

def indexer_limit(dirname,limit):
        os.remove(posting_file)
        os.remove(voc_file)
        files = get_files(dirname)
        vocabulary={}
        document_vector={}
        id_voc=0
        posting={}
        doc_id=0
        pt=0
        size_dirname=0
        size_disk=0

        memory_used= 0

        for file in files:
            with open(file,errors = 'ignore') as file_aux:
                lines = file_aux.readlines()
                file_size= sys.getsizeof(file_aux)
                size_dirname+=sys.getsizeof(file_aux)
            print(limit-memory_used,limit,memory_used,file_size)
            time.sleep(1)
            if ((memory_used+file_size)>limit):
                marge_posting(posting_file,voc_file,vocabulary,posting)
                memory_used=0
                vocabulary={}
                posting={}
            else:
                memory_used+=file_size
            
            docu_voc=[]
            tokens=tokenizar(lines)
            for token in tokens:
                if token not in vocabulary:
                    #print(token)
                    vocabulary[token]=(id_voc,1)
                    docu_voc.append(id_voc)
                    posting[token]=[doc_id]
                    id_voc =id_voc+1
                else:
                    id,doc_freq = vocabulary[token]
                    if id not in docu_voc:
                        doc_freq = doc_freq+1
                        docu_voc.append(id)
                        posting[token].append(doc_id)
                    vocabulary[token]=(id,doc_freq)
                    pt+=doc_freq
            document_vector[file]=docu_voc
            
            doc_id+=1
        # voc_id=[]
        # pt=0
        # for term in sorted(vocabulary.keys()):
        #     df=vocabulary[term]
        #     voc_id.append((term,df[1],pt))
        #     pt+=df[1]*4
        # return (voc_id,posting)
        marge_posting(posting_file,voc_file,vocabulary,posting)
        return(posting_file)

def indexer(dirname):
        # files = listdir(dirname)
        files = get_files(dirname)
        vocabulary={}
        document_vector={}
        id_voc=0
        posting={}
        doc_id=0
        pt=0
        size_dirname=0
        size_disk=0
        for file in files:
            with open(file,errors = 'ignore') as file_aux:
                lines = file_aux.readlines()
                size_dirname+=sys.getsizeof(file_aux)
            
            docu_voc=[]
            tokens=tokenizar(lines)
            for token in tokens:
                if token not in vocabulary:
                    vocabulary[token]=(id_voc,1)
                    docu_voc.append(id_voc)
                    posting[token]=[doc_id]
                    id_voc =id_voc+1
                else:
                    id,doc_freq = vocabulary[token]
                    if id not in docu_voc:
                        doc_freq = doc_freq+1
                        docu_voc.append(id)
                        posting[token].append(doc_id)
                    vocabulary[token]=(id,doc_freq)
                    pt+=doc_freq
            document_vector[file]=docu_voc
            
            doc_id+=1
        voc_id=[]
        pt=0
        for term in sorted(vocabulary.keys()):
            df=vocabulary[term]
            voc_id.append((term,df[1],pt))
            pt+=df[1]*4
        return (voc_id,posting)

def marge_posting(file_posting,voc_file,vocabulary,posting):
    print("merge postin y vocabulario ...")
    
    len_data=len(binary_pack([1],FORMAT_STRUCT))
    voc_id=[]
    new_posting={}
    # size = int(os.path.getsize(file_posting)/len_data) 
    #new_terms = read_voc(voc_file)
    if (os.path.isfile(file_posting) ):
        pt=0
        old_voc = read_voc(voc_file)
        for term in vocabulary.keys():
            if term in old_voc.keys():
                old_df,old_pt = old_voc[term] 
                with open(file_posting,"rb") as index:
                    index.seek(int(old_pt))
                    bin_old_posting = index.read(int(old_df)*len_data)
                    old_posting = struct.unpack(FORMAT_STRUCT.format(int(old_df)),bin_old_posting)
                    new_posting[term]=list(old_posting)
                new_df = int(old_df)

                for postin in posting[term]:
                    
                    if postin not in new_posting[term]:     
                        new_posting[term].append(postin)
                 
                        new_df+=1
                
                voc_id.append((term,new_df,pt))
                pt+=int(new_df)*4
            else:
                new_id ,new_df=vocabulary[term]
                
                voc_id.append((term,new_df,pt))
                pt+=new_df*4
                new_posting[term]=posting[term]
        
        for term in old_voc.keys():
            if term not in new_posting.keys():
                new_df,new_id=old_voc[term]
                voc_id.append((term,new_df,pt))
                new_posting[term]=list(old_posting)

                pt+=int(new_df)*4

    else:

        pt=0
       
        for term in sorted(vocabulary.keys()):
            new_posting[term]=[]
            new_df=0
            for postin in posting[term]:
                if postin not in new_posting[term]:     
                    new_posting[term].append(postin)        
                    new_df+=1

                id ,df=vocabulary[term]
                voc_id.append((term,df,pt))
            
                pt+=df*4

    save_posting(voc_id,new_posting,posting_file,FORMAT_STRUCT)
    save_voc(voc_id,voc_file)


def read_voc(voc_file):
    vocs=[]
    vocs_id={}
    if (os.path.isfile(voc_file)):
        with open(voc_file) as vocabulary:
            lines =vocabulary.readlines()
            for line in lines:
                term=line.split()
                vocs.append(term)
                vocs_id[term[1]]=(term[2],term[3])
    #print(vocs_id,"vocs i")
    return vocs_id

def plot_bar(values,label):
    index= np.arange(len(label))
    plt.bar(index,values)
    plt.xticks(index, label, fontsize=10, rotation=30)
    plt.show()

def save_posting(vocs,posting,path,FORMAT_STRUCT):
    with open(path,"wb") as index:
        for term, value,pt in vocs:
            index.write(binary_pack(posting[term],FORMAT_STRUCT))


def save_voc(vocs,path):
    with open(path,"w") as voc:
        
        for index,(term, value,pt) in enumerate(vocs):

            voc.write(str(index)+" "+str(term)+" "+str(value)+" "+str(pt)+"\n")

# with open("voc.txt","w") as voc:
#     for term, value,pt in vocs:
#         voc.write(str(term)+" "+str(value)+" "+str(pt)+"\n")


# with open("index.bin","rb") as index:
#     size_obj_index=sys.getsizeof(index)
#     tuple_index =binary_unpack(index,FORMAT_STRUCT.format(size))
#     tuple_array = np.array(tuple_index)
#     terms=[]
#     for term, value,pt in vocs:
#         index.seek(pt)
#         docus=index.read(value*len_data)
#         postin=struct.unpack(FORMAT_STRUCT.format(value),docus)



# ###main
# vocs,posting = (indexer(dirname))
# save_index(vocs,posting,"index.bin")
# len_data=len(binary_pack([1]))
# size = int(os.path.getsize("index.bin")/len_data)   
# save_voc(vocs,"voc.txt")


# with open("index.bin","rb") as index:
#     size_obj_index=sys.getsizeof(index)
#     tuple_index =binary_unpack(index,FORMAT_STRUCT.format(size))
#     tuple_array = np.array(tuple_index)
#     terms=[]
#     for term, value,pt in vocs:
#         index.seek(pt)
#         docus=index.read(value*len_data)
#         postin=struct.unpack(FORMAT_STRUCT.format(value),docus)




# # print(os.path.getsize(dirname))

# print("directory size",os.path.getsize(dirname))
# print("directory posting",os.path.getsize("index.bin"))
# print("directory index",os.path.getsize("voc.txt"))
# print("---------------------------------------------")
# print("overhead",((os.path.getsize("index.bin")-os.path.getsize("voc.txt")-os.path.getsize(dirname))/os.path.getsize("index.bin"))/os.path.getsize("index.bin"),"%")
# #print("result",size_obj_index+sys.getsizeof(vocs)-os.path.getsize(dirname))
# #print(vocs)


# vocs.sort(key=operator.itemgetter(1))
# distribution={}
# befor_df=vocs[0][1]
# aux=0
# #print(befor_df)
# for _,df,_ in vocs:
#     if befor_df==df:
#         aux+=1
#     else:
#         distribution[befor_df]=aux
#         aux=1
#         befor_df=df
# #print(distribution)
# # print(vocs)

# plot_bar(distribution.values(),distribution.keys())
