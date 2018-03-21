# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:20:34 2018

@author: Andres

References:
Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
"""

import nltk
import csv

class SpellChecker():

    def __init__(self,text=""):
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        self.dictionary=nltk.FreqDist()
        self.add_words(text)
        self.letters = 'abcdefghijklmnñopqrstuvwxyz'
        
    def add_words(self,text):
        for word in self.tokenizer.tokenize(text):
            self.dictionary[word.lower()] += 1
       
        
    def add_words_count(self,dictionary):
        for k,v in dictionary.items():
            self.dictionary[k]+=v
            
    def probability(self,word):
        return self.dictionary[word]/self.dictionary.B() if self.dictionary else 0
    
    def known(self,words):
        return set(w for w in words if w in self.dictionary)
    
    
    def edits(self,word,n=1):
        if n<1:
            n=1
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in self.letters]
        inserts    = [L + c + R               for L, R in splits for c in self.letters]
        
        res=set(deletes + transposes + replaces + inserts)
        for i in range(1,n):
            res=[e for e1 in res for e in self.edits(e1)]
        return res
    
    def candidates(self,word):
#        return self.known([word]) \
#                .union(self.known(self.edits(word)))   \
#                .union(self.known(self.edits(word,2)))  \
#                .union({word})  
                
        return self.known([word]) \
                or self.known(self.edits(word))  \
                or self.known(self.edits(word,2))  \
                or [word]

                
    
    
    def correct(self,word):
        return max(self.candidates(word),key=self.probability)
    
    
    def correct_sentence(self,sentence):
        return " ".join(self.correct(w) for w in sentence.split(" "))
    

    
if __name__=="__main__":
    
    sp=SpellChecker()
    print("Opening file...")
    with open('CREA_total.txt') as csvfile:
        dictionary = csv.DictReader(csvfile, delimiter='\t')
        w=dictionary.fieldnames[1]
        f=dictionary.fieldnames[2]
        
        
        
        sp.add_words_count({row[w] :int(row[f].replace(",","")) for row in dictionary })
        print(sp.dictionary.most_common(25))    
        
        
    with open('text.txt',encoding="utf8") as csvfile:
        #dictionary = csv.reader(csvfile, delimiter='\t')
        next(csvfile,None)
        next(csvfile,None)

        for r in csvfile:
            sp.add_words(r)

        print(sp.dictionary.most_common(25))    
        
        
        
        
        
        
        