# import boolean
# from luqum.parser import parser
# import boolparser
# import agruptree as Tree
import re
import TAAT 
from modulos.tokenizer import tokenizar


def get_or_queries(query):
    
    for subquery in query.split(' or '):
        yield subquery


def get_and_query(subquery):
    for phrase in subquery.split(' and '):
        yield phrase

def get_not_query(notquery):
        
        # for notq in notquery.split(' NOT |NOT'):
        for notq in re.split(' not |not | ',notquery):
            if not notq == '':
            # print(notq,"notq",notquery,notquery.split(' NOT |NOT'))
                yield notq

def token_query(query):
    query_result=""
    for token in tokenizar(query.split()):
        query_result += token+" "
        # print(query_result)
    return query_result

def find_wp(query,indice,FORMAT_STRUCT,postin_list):
    # print(query,"Query iniciada")
    result=[]
    or_conjunto =set()
    for subquery in get_or_queries(query):
        and_conjunto=set()
        not_conjunto=set()
        # print(subquery)


        for phrase in get_and_query(subquery):
            # print(phrase,"--")
            if "NOT" in phrase.split():
                for term in get_not_query(phrase):
                    docs=TAAT.taat_wp(term,indice,FORMAT_STRUCT,postin_list,subquery)
                    if len(not_conjunto)==0:
                        for docs_id in docs:
                            # print(docs_id)
                            not_conjunto.add(docs_id)
                        # print(not_conjunto,len(not_conjunto))
                    else:
                        not_conjunto.union(docs)
                    # print(term,"term",not_conjunto)
            else:
                if len(and_conjunto)==0:
                    docs=TAAT.taat_wp(phrase.strip(),indice,FORMAT_STRUCT,postin_list,subquery)
                    for id in docs:
                        and_conjunto.add(id)
                    # print(and_conjunto)
                else:
                    docs=TAAT.taat_wp(phrase,indice,FORMAT_STRUCT,postin_list,subquery)
                    and_conjunto= and_conjunto.intersection(docs)
            # print(and_conjunto)
        # print(not_conjunto)
        or_conjunto = or_conjunto.union(and_conjunto)
        or_conjunto = or_conjunto.difference(not_conjunto)
    result={}
    # for item in or_conjunto:
    #     if item in 
    return(list(or_conjunto),"result")

def find(query,indice,FORMAT_STRUCT,postin_list):
    # print(query,"Query iniciada")
    result=[]
    or_conjunto =set()
    for subquery in get_or_queries(query):
        and_conjunto=set()
        not_conjunto=set()
        # print(subquery)


        for phrase in get_and_query(subquery):
            # print(phrase,"--")
            if "NOT" in phrase.split():
                for term in get_not_query(phrase):
                    docs=TAAT.taat(term,indice,FORMAT_STRUCT,postin_list)
                    if len(not_conjunto)==0:
                        for docs_id in docs:
                            # print(docs_id)
                            not_conjunto.add(docs_id)
                        # print(not_conjunto,len(not_conjunto))
                    else:
                        not_conjunto.union(docs)
                    # print(term,"term",not_conjunto)
            else:
                if len(and_conjunto)==0:
                    docs=TAAT.taat(phrase.strip(),indice,FORMAT_STRUCT,postin_list) 
                    for id in docs:
                        and_conjunto.add(id)
                    # print(and_conjunto)
                else:
                    docs=TAAT.taat(phrase,indice,FORMAT_STRUCT,postin_list)
                    and_conjunto= and_conjunto.intersection(docs)
            # print(and_conjunto)
        # print(not_conjunto)
        or_conjunto = or_conjunto.union(and_conjunto)
        or_conjunto = or_conjunto.difference(not_conjunto)
    return(list(or_conjunto),"result")


def find_vectorial(query,indice,FORMAT_STRUCT,postin_list,frecuencia,docs_t):
    # print(query,"Query iniciada")
    result=[]
    or_conjunto =set()
    for subquery in get_or_queries(query):
        and_conjunto=set()
        not_conjunto=set()
        # print(subquery)


        for phrase in get_and_query(subquery):
            # print(phrase,"--")
            if "NOT" in phrase.split():
                for term in get_not_query(phrase):
                    docs=TAAT.taat_idf(term,indice,FORMAT_STRUCT,postin_list,frecuencia,docs_t) 
                    if len(not_conjunto)==0:
                        for docs_id in docs:
                            # print(docs_id)
                            not_conjunto.add(docs_id)
                        # print(not_conjunto,len(not_conjunto))
                    else:
                        not_conjunto.union(docs)
                    # print(term,"term",not_conjunto)
            else:
                if len(and_conjunto)==0:
                    docs=TAAT.taat_idf(phrase.strip(),indice,FORMAT_STRUCT,postin_list,frecuencia,docs_t)
                    for id in docs:
                        and_conjunto.add(id)
                    # print(and_conjunto)
                else:
                    docs=TAAT.taat_idf(phrase,indice,FORMAT_STRUCT,postin_list,frecuencia,docs_t)
                    and_conjunto= and_conjunto.intersection(docs)
            # print(and_conjunto)
        # print(not_conjunto)
        or_conjunto = or_conjunto.union(and_conjunto)
        or_conjunto = or_conjunto.difference(not_conjunto)
    result={}
    print(or_conjunto)
    for r,doc_id in or_conjunto:
        if doc_id not in result.keys():
            result[doc_id]=r
        else:
            result[doc_id]+=r
    # return(list(or_conjunto),"result")
    return result
    # return(list(or_conjunto),"result")



def find_vectorial_2(query,indice,FORMAT_STRUCT,postin_list,frecuencia,docs_t,docs_normal):
    # print(query,"Query iniciada")
    result=[]
    or_conjunto =set()
    for subquery in get_or_queries(query):
        and_conjunto=set()
        not_conjunto=set()
        # print(subquery)


        for phrase in get_and_query(subquery):
            # print(phrase,"--")
            if "NOT" in phrase.split():
                for term in get_not_query(phrase):
                    docs=TAAT.taat_idf_2(term,indice,FORMAT_STRUCT,postin_list,frecuencia,docs_t,docs_normal) 
                    if len(not_conjunto)==0:
                        for docs_id in docs:
                            # print(docs_id)
                            not_conjunto.add(docs_id)
                        # print(not_conjunto,len(not_conjunto))
                    else:
                        not_conjunto.union(docs)
                    # print(term,"term",not_conjunto)
            else:
                if len(and_conjunto)==0:
                    docs=TAAT.taat_idf_2(phrase.strip(),indice,FORMAT_STRUCT,postin_list,frecuencia,docs_t,docs_normal)
                    for id in docs:
                        and_conjunto.add(id)
                    # print(and_conjunto)
                else:
                    docs=TAAT.taat_idf_2(phrase,indice,FORMAT_STRUCT,postin_list,frecuencia,docs_t,docs_normal)
                    and_conjunto= and_conjunto.intersection(docs)
            # print(and_conjunto)
        # print(not_conjunto)
        or_conjunto = or_conjunto.union(and_conjunto)
        or_conjunto = or_conjunto.difference(not_conjunto)
    result={}
    # print(or_conjunto)
    for r,doc_id in or_conjunto:
        if doc_id not in result.keys():
            result[doc_id]=r
        else:
            result[doc_id]+=r
    # return(list(or_conjunto),"result")
    return result
    # return(list(or_conjunto),"result")


def find_memory(query,indice,FORMAT_STRUCT,postin_list):
    # print(query,"Query iniciada")
    result=[]
    or_conjunto =set()
    for subquery in get_or_queries(query):
        and_conjunto=set()
        not_conjunto=set()
        # print(subquery)


        for phrase in get_and_query(subquery):
            # print(phrase,"--")
            if "NOT" in phrase.split():
                for term in get_not_query(phrase):
                    docs=TAAT.taat_memory(term,indice,FORMAT_STRUCT,postin_list)
                    if len(not_conjunto)==0:
                        for docs_id in docs:
                            # print(docs_id)
                            not_conjunto.add(docs_id)
                        # print(not_conjunto,len(not_conjunto))
                    else:
                        not_conjunto.union(docs)
                    # print(term,"term",not_conjunto)
            else:
                if len(and_conjunto)==0:
                    docs=TAAT.taat_memory(phrase.strip(),indice,FORMAT_STRUCT,postin_list)
                    for id in docs:
                        and_conjunto.add(id)
                    # print(and_conjunto)
                else:
                    docs=TAAT.taat_memory(phrase,indice,FORMAT_STRUCT,postin_list)
                    and_conjunto= and_conjunto.intersection(docs)
            # print(and_conjunto)
        # print(not_conjunto)
        or_conjunto = or_conjunto.union(and_conjunto)
        or_conjunto = or_conjunto.difference(not_conjunto)
    return(list(or_conjunto))

# string=" 2 1 AND 1 0 2 AND NOT 2 "

# # #print(get_paranteses_query(string))

# # # print(get_paranteses_query(string))
# find(string)