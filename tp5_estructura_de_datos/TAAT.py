import heapq

def Ranking_funtion():
    return 1

def getPostings(term):
    return([1,2])

def heapsort(iterable):
     h = []
     for value in iterable:
         heapq.heappush(h, value)
     return [heapq.heappop(h) for i in range(len(h))]

def taat(query,Indice,k_heap):

    postings=[]
    document_acum={}
    Heap = []
    heapq.heapify(Heap)

    for term in query:
        # postings.extend(getPostings(term))
        postings.append(getPostings(term))


    for posting in postings:
        for doc_id in posting:
            document_acum[doc_id]+=Ranking_funtion

    for term,acum in document_acum.items():
        heapq.heappush(Heap,(acum,term))
    
    return heapsort(Heap)