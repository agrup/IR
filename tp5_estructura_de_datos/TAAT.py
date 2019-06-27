import heapq
from structure import *
import math 

def Ranking_funtion_idf(term,indice,frecuencia,docs):
    # print(frecuencia[term],term,indice[term][0])
    print(docs,indice[term][0],"casa",term)
    t_idf = docs /int(indice[term][0])
    return math.log(t_idf,2)
    # print(term)
    # return frecuencia[term]
    # return 1
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



def taat_idf(query,Indice,FORMAT_STRUCT,postin_list,frecuencia,docs):

    postings=[]
    document_acum={}
    Heap = []
    heapq.heapify(Heap)

    # for term in query:
    #     # postings.extend(getPostings(term))
    #     postings.append(getPostings(term,Indice,FORMAT_STRUCT))
    postings.append(getPostings(query,Indice,FORMAT_STRUCT,postin_list))
    # print(frecuencia)

    for posting in postings:
        for doc_id in posting:
            # print(doc_id)
            if doc_id in document_acum.keys():
                document_acum[doc_id]+=Ranking_funtion_idf(query,Indice,frecuencia,docs)
            else:
                document_acum[doc_id]=Ranking_funtion_idf(query,Indice,frecuencia,docs)



    for term,acum in document_acum.items():
        heapq.heappush(Heap,(acum,term))
    # print(heapsort(Heap))
    return heapsort(Heap)

def taat_wp(query,Indice,FORMAT_STRUCT,postin_list,query_list):

    # print(query, query_list,"param")
    postings=[]
    document_acum={}
    Heap = []
    heapq.heapify(Heap)
    print(query,"query")
    # postings.append(getPostings(query,Indice,FORMAT_STRUCT,postin_list))
    if len(query.split())>1:
        for term in query.split():
            for o_term in query.split():
                if term != o_term:
                    for doc_id in postin_list[term]:
                        if (o_term,doc_id) in postin_list.keys():
                            for ub in postin_list[(term,doc_id)]:
                                for o_ub in postin_list[(o_term,doc_id)]:
                                    print(ub,o_ub,doc_id)
                                    if ub in range(o_ub -3,o_ub+3):
                                        if doc_id in document_acum.keys():
                                            document_acum[str(doc_id)]+=Ranking_funtion()
                                        else:
                                            document_acum[str(doc_id)]=1

    

        for term,acum in document_acum.items():
            heapq.heappush(Heap,(acum,term))
        return heapsort(Heap)
    else:
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

