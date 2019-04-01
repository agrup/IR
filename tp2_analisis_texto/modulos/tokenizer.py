
import re
from nltk.stem import SnowballStemmer 
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

LEN_CHIMIST=2
MIN_TOKEN = 2
MAX_TOKEN = 20
numero_regex = r"^([0-9]+[,])*[0-9]([.][0-9]+)?"
#numero_regex = r"(?<![a-zA-Z])\d+((\.|,)\d+)?(?![a-zA-Z])"
abreviatura = r'(?:[A-Z]\.)+'

mail_regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"


url_regex=r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
nombre_regex=r'[A-Z][a-z]+ [A-Z][a-z]*'

def tokenizar(lines):
    tokens = []

    for line in lines:
        line = re.sub(r'[^a-zA-Z0-9]', ' ', line)
        #line = re.sub(r'[A-Z][a-z]?\d*|\(.*?\)\d+', ' ', line)
        words = line.split()
        for word in words:
            if not (len(word) < MIN_TOKEN or len(word) > MAX_TOKEN):
                word = word.lower()
                tokens.append(word)
    return tokens    

def tokenizar_quimica(lines):
    tokens = []

    for line in lines:
        #line = re.sub(r'[^a-zA-Z]', ' ', line)
        #line = re.sub(r'[A-Z][a-z]?\d*|\(.*?\)\d+', ' ', line)
        line = re.sub(r'/(\(?)([A-Z])([a-z]*)([0-9]*)(\))?([0-9]*)/g', ' ', line)

        words = line.split()
        for word in words:
            if len(word) > LEN_CHIMIST:
                word = word.lower()
                tokens.append(word)
            else:
 
                word = re.sub(r'[^A-Za-z]','',word)
                if word:
                    word = word.lower()
                    tokens.append(word)
 
    return tokens  


def tokenizar_stemer_sb(lines):
    tokens = []

    ps = SnowballStemmer('spanish')

    for line in lines:
        line = re.sub(r'[^a-zA-Z]', ' ', line)
        words = line.split()
        for word in words:
            if not (len(word) < MIN_TOKEN or len(word) > MAX_TOKEN):
                word = word.lower()
                word = ps.stem(word)
                tokens.append(word)
    return tokens    


def tokenizar_porter(lines):
    tokens = []

    ps = PorterStemmer()

    for line in lines:
        line = re.sub(r'[^a-zA-Z]', ' ', line)
        words = line.split()
        for word in words:
            if not (len(word) < MIN_TOKEN or len(word) > MAX_TOKEN):
                word = word.lower()
                word = ps.stem(word)
                tokens.append(word)
    return tokens 

def tokenizar_lancaster(lines):
    tokens = []

    ps = LancasterStemmer()

    for line in lines:
        line = re.sub(r'[^a-zA-Z]', ' ', line)
        words = line.split()
        for word in words:
            if not (len(word) < MIN_TOKEN or len(word) > MAX_TOKEN):
                word = word.lower()
                word = ps.stem(word)
                tokens.append(word)
    return tokens     

def get_abreviaturas(text):
    abreviaturas = []

    for line in text:
        #print(line)
        abreviaturas.extend(tokenizar_special(line,abreviatura))
    
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

def get_nombres_propios(lines):
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
        