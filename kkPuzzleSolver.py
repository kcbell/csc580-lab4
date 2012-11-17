'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 15, 2012

@author: Toshi
'''
import re, nltk, string, urllib, os

from nltk.corpus import brown
from nltk.chunk import RegexpParser


URL = "http://philosophy.hku.hk/think/logic/knight.php"
PARAM = "qno=%d"
NUM_PUZZLES = 25

def getPuzzle(html):
    strPuzzle = ""
    title = "<title>Knights and Knaves</title>"
    bigTag = "<p>"
    endTag = "</p>"
    entTag = "<entry>"
    numParas = 0
    idx = html.find(title)
    if idx > -1:
        html = html[idx+len(title):]
    while numParas < 3 and len(html) > 0:
        idx1 = html.find(bigTag)
        if idx1 < 0:
            break
        if numParas == 1:
            idx1 = html.find(entTag) + len(entTag)
        else:
            idx1 = idx1 + len(bigTag)
        idx2 = html.find(endTag)
        if idx2 < 0:
            break
        strPuzzle += html[idx1:idx2]
        html = html[idx2 + len(endTag):]
        numParas += 1

    return strPuzzle.strip().replace("`", "'")

def getSecondPara(puz):
    paras = []
    

def parsePuz(puz):
    myDict = {}
    entities = []
    #para = getSecondPara(puz)
    sents = nltk.sent_tokenize(puz)
    #print sents
    #count = 1
    for sent in sents:
        if len(entities) == 0:
            entities = getEntities(sent)
        else:
            tup = parseSent(entities, sent)
            if tup[0] != None:
                myDict[tup[0]] = tup[1]

            if len(myDict.keys()) == len(entities):
                break
                      
        #count += 1
        
   
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
    
    entity = None
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
                entity = match.group(1)
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

def openFile(f):
    input_file = open(f,'r')
    puz = input_file.read()
    input_file.close()
    return puz
            
def main():
    while True:
        source = raw_input('\n Please specify the source {w(web)|f(file)|t(type)}: ')
        if source == "f":
            f = raw_input(' Please specify the file: ')
            if len(f) > 0:
                puz = openFile(f)
                print puz
                (entities, puzDict) = parsePuz(puz)
                print entities, puzDict
                #call Jake's Function(entities, puzDict)
        elif source == "t":
            puz = raw_input(' Please type the puzzle(no newline char please): ')
            if len(puz) > 0:
                print puz
                (entities, puzDict) = parsePuz(puz)
                print entities, puzDict
                #call Jake's Function(entities, puzDict)
        else:
            for i in xrange(1, NUM_PUZZLES):
                puz = getPuzzle(urllib.urlopen(URL, PARAM % i).read())
                if len(puz) == 0:
                    print "Error: No puzzle was read!"
                    break
                print puz
                #puz = "You meet two inhabitants: Zoey and Mel.  Zoey tells you that Mel is a knave.  Mel says, 'Neither Zoey nor I are knaves.'"
                (entities, puzDict) = parsePuz(puz)
                print entities, puzDict
                #call Jake's Function(entities, puzDict)
            break # break from while loop

        val = raw_input('\n Do you want to solve another puzzle? {y|n}: ')
        if val == "n":
            break #break from while loop

if __name__ == '__main__':
    main()
    
