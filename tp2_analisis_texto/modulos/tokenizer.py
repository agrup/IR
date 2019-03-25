import re

def tokenizar(lines):
    tokens = []
    for line in lines:
        words = line.split()
        for word in words:
            tokens.append(word)
    return tokens    
