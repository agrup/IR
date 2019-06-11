import heapq
from structure import *

def Ranking_funtion():
    return 1

def getPostings(term,indice,FORMAT_STRUCT,postin_list):
    if term in indice.keys():
        len_data=len(binary_pack([1],FORMAT_STRUCT))

        count, pt = indice[term]
        with open(postin_list,"rb") as index:
        # with open("posting_list.bin","rb") as index:
            # print(int(pt),int(count))
            index.seek(int(pt))
            docus=index.read(int(count)*len_data)

            postin=struct.unpack(FORMAT_STRUCT.format(count),docus)
    else:
        postin=[]
    return(postin)

def getPostings_memory(term,indice,FORMAT_STRUCT,postin_list):
    if term in indice.keys():
        len_data=len(binary_pack([1],FORMAT_STRUCT))

        count, pt = indice[term]
        # with open(postin_list,"rb") as index:
        # with open("posting_list.bin","rb") as index:
            # print(int(pt),int(count))
            # index.seek(int(pt))
        # docus=index.read(int(count)*len_data)

            # postin=struct.unpack(FORMAT_STRUCT.format(count),docus)
    else:
        postin=[]
    return(postin)


def heapsort(iterable):
     h = []
     for value in iterable:
         heapq.heappush(h, value)
     return [heapq.heappop(h) for i in range(len(h))]

def taat(query,Indice,FORMAT_STRUCT,postin_list):

    postings=[]
    document_acum={}
    Heap = []
    heapq.heapify(Heap)

    # for term in query:
    #     # postings.extend(getPostings(term))
    #     postings.append(getPostings(term,Indice,FORMAT_STRUCT))
    postings.append(getPostings(query,Indice,FORMAT_STRUCT,postin_list))


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


def taat_memory(query,Indice,FORMAT_STRUCT,postin_list):

    postings=[]
    document_acum={}
    Heap = []
    heapq.heapify(Heap)

    # postings.append(getPostings(query,Indice,FORMAT_STRUCT,postin_list))
    if query in postin_list:
        for posting in postin_list[query]:
            for doc_id in [posting]:
                if doc_id in document_acum.keys():
                    document_acum[str(doc_id)]+=Ranking_funtion()
                else:
                    document_acum[str(doc_id)]=Ranking_funtion()

        for term,acum in document_acum.items():
            heapq.heappush(Heap,(acum,term))
        return heapsort(Heap)
    else:
        return heapsort(Heap)


# vocs,posting = (indexer(dirname))

