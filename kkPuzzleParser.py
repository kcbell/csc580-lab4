'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 15, 2012

@author: Toshi
'''
import re, nltk, string, urllib, os

from nltk.corpus import brown
from nltk.chunk import RegexpParser

def parsePuz(puz):
    myDict = {}
    entities = []
    sents = nltk.sent_tokenize(puz)
    for sent in sents:
        if len(entities) == 0:
            entities = getEntities(sent)
        else:
            tup = parseSent(entities, sent)
            if tup[0] != None:
                myDict[tup[0]] = tup[1]
            if len(myDict.keys()) == len(entities):
                break
    return entities, myDict

def getEntities(sent):
    entities = []
    words = sent.split()
    tagger = getPOSTagger()
    tagged = tagger.tag(words)
    NP = [w for (w,t) in tagged if t == "NN" or t == "NP"]
    #print NP
    for w in NP:
        if w.lower() != "knights" and w.lower() != "knaves":
            match = re.match("(^[A-Z]\w*).?", w)
            if match != None:
                entities.append(match.group(1))
    #print entities
    return entities

def getPOSTagger():
    # lazy init
    if not hasattr(getPOSTagger, 'tagger'):
        brown_tagged_sents = brown.tagged_sents(categories='news',simplify_tags=True)
        t0 = nltk.DefaultTagger('NN')
        t1 = nltk.UnigramTagger(brown_tagged_sents, backoff=t0)
        getPOSTagger.tagger = nltk.BigramTagger(brown_tagged_sents, backoff=t1)
    return getPOSTagger.tagger

def parseSent(entities, sent):
    queries = [
        "^(\w*)[^\w]claims,[^\w]'((\w*[^\w]+)*)'?",
        "^(\w*)[^\w]claims[^\w]that[^\w]((\w*[^\w]+)*)",
        "^(\w*)[^\w]says[^\w]that[^\w]((\w*[^\w]+)*)",
        "^(\w*)[^\w]says,[^\w]'((\w*[^\w]+)*)'?",
        "^(\w*)[^\w]tells[^\w]you[^\w]that[^\w]((\w*[^\w]+)*)",
        "^(\w*)[^\w]tells[^\w]you,[^\w]'((\w*[^\w]+)*)'?"
        ]
    
    statement = None
    idx = None
    
    sent = clean(sent)
    if sent == None:
        return (idx, statement)
    
    for q in queries:
        match = re.match(q, sent, re.IGNORECASE)
        if match != None:
            try:
                idx = entities.index(match.group(1))
                statement = match.group(2)
                #print entity, idx, statement
                break
            except:
                print "error"
                break

    return (idx, statement)

def clean(sent):
    idx = 0
    for c in sent:
        if c.isalpha():
            return sent[idx:]
        else:
            idx += 1
    #print "None:" + sent
    return None

def main():
    try:
        while True:
            entities, puzDict = parsePuz(raw_input().strip().replace("`", "'"))
            print entities
            for entity, val in puzDict.iteritems():
                print entity, ":", val 
    except EOFError:
        print
        

if __name__ == '__main__':
    main()