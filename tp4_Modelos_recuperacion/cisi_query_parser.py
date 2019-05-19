import re
import sys

dircisi = "/home/agu/Unlu/IR/colecciones/cisi/"
QRY="CISI.QRY"
REL = "CISI.REL"
TERM= "CISI.terms"

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
                        i+=1
                    
                    #print(newQry)
                    queries[id]=newQry
                
                id+=1
        with open(QRY+".txt",'a',encoding='utf-8') as qry_result:
            for query, terms in queries.items():
                #print("id qry",query)
                #print("terminos",str(terms))
                qry_str=""
                qry_result.write('<TOP>\n')
                qry_result.write('<NUM>'+str(query)+'</NUM>\n')
                qry_result.write('<TITLE>')
                #qry_result.write(str(query))
                for term in terms:
                    qry_str+=term+" "
                #print(qry_str)
                qry_result.write(qry_str)
                qry_result.write('</TITLE>\n')
                qry_result.write('</TOP>\n')
        #print(queries)
    except IOError as e:
        print (e)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        parse_query(sys.argv[1])
    else:
        print('Invalid params.\n\tUse: python '+sys.argv[0]+ ' name_file.ALL')