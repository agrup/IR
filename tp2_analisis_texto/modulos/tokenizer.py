import unidecode
import re



MIN_TOKEN = 2
MAX_TOKEN = 20
numero_regex = r"^([0-9]+[,])*[0-9]([.][0-9]+)?"
#numero_regex = r"(?<![a-zA-Z])\d+((\.|,)\d+)?(?![a-zA-Z])"
abreviatura = r"[A-Za-z]\.([A-Za-z0-9]\.)+"
mail_regex=""
url_regex=""
nombre_regex=""

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
        abreviaturas.append(tokenizar_special(line,abreviatura))
    #print(abreviaturas)
    return abreviaturas

def get_numero(lines):
    numeros = []
    for line in lines:
        numeros.append(tokenizar_special(line,numero_regex))
    return numeros




def get_url(lines):
    urls = []
    for line in lines:
        urls.append(tokenizar_special(line,url_regex))
    return urls

def get_mail(lines):
    mails=[]
    for line in lines:
        mails.append(tokenizar_special(line,mail_regex))
    return mails    

def get_nombres(lines):
    nombres=[]
    for line in lines:
        nombres.append(tokenizar_special(line,nombre_regex))
    return nombres    



def tokenizar_special(text,regex):
    tokens = []

    for token in re.finditer(regex,text):
        t = token.group(0)
       
        if not (len(t) < MIN_TOKEN or len(t) > MAX_TOKEN):
            tokens.append(t)
    return tokens    
        