import sys

dirREL="CISI.REL"
dircisi = "/home/agu/Unlu/IR/colecciones/cisi/"

def parse_rel(dircisi):
    try:
        with open(dircisi+dirREL, 'r', encoding="utf-8") as rel,\
        open(dirREL+".txt", 'w', encoding="utf-8") as rel_result:
            lines = rel.readlines()
            for l in lines:
                l = l.split()
                rel_result.write(l[0]+'\t0'+'\t'+l[1]+'\t1\n')


    except IOError as e:
        print (e)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        parse_rel(sys.argv[1])
    else:
        print('Invalid params.\n\tUse: python '+sys.argv[0]+ ' name_file.ALL')