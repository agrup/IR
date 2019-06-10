import heapq
from structure import *

def Ranking_funtion():
    return 1

def getPostings(term,indice,FORMAT_STRUCT):
    if term in indice.keys():
        len_data=len(binary_pack([1],FORMAT_STRUCT))
        count, pt = indice[term]
        with open("posting_list.bin","rb") as index:
            # print(int(pt),int(count))
            index.seek(int(pt))
            docus=index.read(int(count)*len_data)
            # tuple_index =binary_unpack(index,FORMAT_STRUCT.format(int(count)))
            # tuple_array = np.array(tuple_index)
            postin=struct.unpack(FORMAT_STRUCT.format(count),docus)
    else:
        # print(term,"termmmm")
        postin=[]
    return(postin)

def heapsort(iterable):
     h = []
     for value in iterable:
         heapq.heappush(h, value)
     return [heapq.heappop(h) for i in range(len(h))]

def taat(query,Indice,FORMAT_STRUCT):

    postings=[]
    document_acum={}
    Heap = []
    heapq.heapify(Heap)

    # for term in query:
    #     # postings.extend(getPostings(term))
    #     postings.append(getPostings(term,Indice,FORMAT_STRUCT))
    postings.append(getPostings(query,Indice,FORMAT_STRUCT))


    for posting in postings:
        for doc_id in posting:
            # print(doc_id)
            if doc_id in document_acum.keys():
                document_acum[doc_id]+=Ranking_funtion()
            else:
                document_acum[doc_id]=Ranking_funtion()

    for term,acum in document_acum.items():
        heapq.heappush(Heap,(acum,term))
    # print(heapsort(Heap))
    return heapsort(Heap)

#dirname="/home/agu/Unlu/IR/colecciones/RI-tknz-data"


# vocs,posting = (indexer(dirname))

