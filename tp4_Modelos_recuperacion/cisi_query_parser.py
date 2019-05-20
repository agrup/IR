import re
import sys

dircisi = "/home/agu/Unlu/IR/colecciones/cisi/"
QRY="CISI.QRY"
REL = "CISI.REL"
TERM= "CISI.terms"
QRY_ONCE="CISI_ONCE.QRY"

def parse_query(dircisi):
    try:

        qrys = []
        with open(dircisi+REL, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            for l in lines:
                qrys.append(int(l.split()[0]))

        terms = {}
        with open(dircisi+TERM, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            for l in lines:
                l = l.split()
                terms[l[0]] = float(l[2])
        #print(qrys,terms)


        queries = {}
        with open(dircisi+QRY, 'r', encoding="utf-8") as qrys:
            lines = qrys.readlines()

            id = 1
            i = 0

            while i < len(lines):
                #print(lines[i])
                if lines[i][0:2] == '.I':
                    #print(lines[i])
                    i += 1
                    newQry = []
                    newQry_once=[]
                    tmp = {}
                    #print("new query",id)
                    #queries[id]
                    while i < len(lines) and lines[i][0:2] != '.I':
                        
                        newterms = lines[i].lower()
                        newterms = re.sub('[\?\.,\-\(\)\"]', ' ', newterms)
                        #print (newterms)
                        for term in newterms.split():
                            if term in terms:
                                newQry.append(term)
                                if term not in newQry_once:
                                    newQry_once.append(term)             
                        i+=1
                    
                    #print(newQry)
                    queries[id]=(newQry , newQry_once)
                    #queries[id]=(newQry)
                    
                
                id+=1
        with open(QRY+".txt",'a',encoding='utf-8') as qry_result,\
            open(QRY_ONCE+".txt",'a',encoding='utf-8') as qry_once_result:
            for query, terms_tup in queries.items():
                #print("id qry",query)
                #print("terminos",str(terms))
                #print(terms)
                qry_str=""
                qry_once_str=""
                
                #termino repetidos
                qry_result.write('<TOP>\n')
                qry_result.write('<NUM>'+str(query)+'</NUM>\n')
                qry_result.write('<TITLE>')

                #terminos no repetidos
                qry_once_result.write('<TOP>\n')
                qry_once_result.write('<NUM>'+str(query)+'</NUM>\n')
                qry_once_result.write('<TITLE>')

                #qry_result.write(str(query))

                terms , terms_once = terms_tup

                for term in terms:
                    qry_str+=term+" "
                
                for term in terms_once:
                    qry_once_str+=term+" "
                #print(qry_str)

                #terminos repetidos
                qry_result.write(qry_str)
                qry_result.write('</TITLE>\n')
                qry_result.write('</TOP>\n')
                
                #terminos sin repetir
                qry_once_result.write(qry_once_str)
                qry_once_result.write('</TITLE>\n')
                qry_once_result.write('</TOP>\n')

        #print(queries)
    except IOError as e:
        print (e)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        parse_query(sys.argv[1])
    else:
        print('Invalid params.\n\tUse: python '+sys.argv[0]+ ' name_file.ALL')