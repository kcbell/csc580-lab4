'''
Pulls the knights and knaves puzzles from http://philosophy.hku.hk/think/logic/knight.php

Created on Nov 9, 2012

@author: Karl
'''
import re, nltk, string, urllib

from nltk.corpus import brown
from nltk.chunk import RegexpParser


URL = "http://philosophy.hku.hk/think/logic/knight.php"
PARAM = "qno=%d"
NUM_PUZZLES = 25
PATTERN = ".*<entry>([^<]*)</p>.*"

def getPuzzle(html):
    match = re.match(PATTERN, html, re.DOTALL)
    return match.group(1).strip().replace("`", "'")

def parsePuz(puz):
    myDict = {}
    sents = nltk.sent_tokenize(puz)
    #print sents
    count = 1
    for sent in sents:
        if count == 1:
            entities = getEntities(sent)
        else:
            tup = parseSent(entities, sent)
            if tup[0] != None:
                myDict[tup[0]] = tup[1]
                
        count += 1
        
   
    return entities, myDict
    


def getEntities(sent):
    entities = []
    words = sent.split()
    tagger = getPOSTagger()
    tagged = tagger.tag(words)
    NP = [w for (w,t) in tagged if t == "NN" or t == "NP"]
    #print NP
    for w in NP:
        if w != "You":
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
                        
            
def main():
    for i in xrange(1, NUM_PUZZLES):
        puz = getPuzzle(urllib.urlopen(URL, PARAM % i).read())
        print puz
        #puz = "You meet two inhabitants: Zoey and Mel.  Zoey tells you that Mel is a knave.  Mel says, 'Neither Zoey nor I are knaves.'"
        (entities, puzDict) = parsePuz(puz)
        print entities, puzDict
        #call Jake's Function(entities, puzDict)

if __name__ == '__main__':
    main()
    
