import unidecode
import re



MIN_TOKEN = 2
MAX_TOKEN = 20


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
