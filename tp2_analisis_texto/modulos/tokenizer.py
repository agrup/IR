import unidecode
import re



MIN_TOKEN = 2
MAX_TOKEN = 20
numero_regex = r"^([0-9]+[,])*[0-9]([.][0-9]+)?"
#numero_regex = r"(?<![a-zA-Z])\d+((\.|,)\d+)?(?![a-zA-Z])"
abreviatura = r"[A-Z][a-z]+\."

mail_regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"


url_regex=r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
nombre_regex=r'[A-Z][a-z]+ [A-Z][a-z]*'

def tokenizar(lines):
    tokens = []

    for line in lines:
        line = re.sub(r'[^a-zA-Z]', ' ', line)
        words = line.split()
        for word in words:
            if not (len(word) < MIN_TOKEN or len(word) > MAX_TOKEN):
                word = word.lower()
                tokens.append(word)
    return tokens    

def get_abreviaturas(text):
    abreviaturas = []

    for line in text:
        #print(line)
        abreviaturas.extend(tokenizar_special(line,abreviatura))
    #print(abreviaturas)
    return abreviaturas

def get_numero(lines):
    numeros = []
    for line in lines:
        numeros.extend(tokenizar_special(line,numero_regex))
    return numeros




def get_url(lines):
    urls = []
    for line in lines:
        urls.extend(tokenizar_special(line,url_regex))
    return urls

def get_mail(lines):
    mails=[]
    for line in lines:
        aux = tokenizar_special(line,mail_regex)
        if not len(aux)==0:
            mails.extend(aux)
    return mails    

def get_nombres(lines):
    nombres=[]
    for line in lines:
        aux = tokenizar_special(line,nombre_regex)
        if len(aux):
            nombres.extend(aux)
    return nombres    



def tokenizar_special(text,regex):
    tokens = []
    token = re.findall(regex,text)
    tokens.extend(token)
    return tokens    
        