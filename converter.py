'''
Created on 11/12/2012

@author: Jake
'''

import logic
import nltk
import re

def initializeDict():
    sentDict = {}
    sentDict['entities'] = []
    sentDict['relations'] = []
    sentDict['class'] = []
    return sentDict

def parseTree(sentDict, tree):
    prevRB = ''
    for child in tree:
        if type(child) == nltk.tree.Tree:
            parseTree(sentDict, child)
        elif type(child) == tuple:
            if (child[0] == 'Zed' or child[1] == 'NNP' or child[1] == 'PRP') and (child[0].lower() != 'it'):
                sentDict['entities'].append(child[0])
            elif 'knight' in child[0] or 'knave' in child[0]:
                sentDict['class'].append(child[0])
            elif child[1] == 'CD':
                if prevRB.lower() == 'exactly':
                    sentDict['entities'].append(prevRB.lower() + '-' + child[0])
            else:
                sentDict['relations'].append(child[0])
            
            if child[1] == 'RB':
                prevRB = child[0]
    return sentDict

def createChunkTree(str):
    sent = nltk.word_tokenize(str)
    sent = nltk.pos_tag(sent)
    return nltk.ne_chunk(sent, binary=True)

def getNum(str):
    if str == 'one':
        return 1
    elif str == 'two':
        return 2

def createLogicStmt(entities, key, sentDict):
    pronounList = ['I']
    negationList = ['not', 'neither', 'nor', 'false']
    list = []
    negation = False
    existential = ''

    for neg in negationList:
        if neg in sentDict['relations']:
            negation = True
            break

    for ent in sentDict['entities']:
        if 'exactly-' in ent:
            existential = ent
            break 
    
    if (not sentDict['class']) and ('same' in sentDict['relations'] or 'different' in sentDict['relations']):
        refs = []
        for ent in sentDict['entities']:
            if ent in pronounList:
                refs.append(key)
            else:
                refs.append(entities.index(ent))
        if 'same' in sentDict['relations']:
            list.append(logic.BinaryStmt(logic.KnightStmt(refs[0]), logic.BinaryStmt.EQ, logic.KnightStmt(refs[1]))) if (not negation) else list.append(logic.BinaryStmt(logic.KnightStmt(refs[0]), logic.BinaryStmt.XOR, logic.KnightStmt(refs[1])))
        else:
            list.append(logic.BinaryStmt(logic.KnightStmt(refs[0]), logic.BinaryStmt.XOR, logic.KnightStmt(refs[1]))) if (not negation) else list.append(logic.BinaryStmt(logic.KnightStmt(refs[0]), logic.BinaryStmt.EQ, logic.KnightStmt(refs[1])))
    elif existential != '':
        index = key
        ks = logic.KnightStmt(index)
        if 'knight' in sentDict['class'] or 'knights' in sentDict['class']:
            es = logic.ExistsStmt(logic.ExistsStmt.EQ, getNum(existential.split('-')[1]), ks)
        else:
            es = logic.ExistsStmt(logic.ExistsStmt.EQ, getNum(existential.split('-')[1]), logic.UnaryStmt(logic.UnaryStmt.NOT, ks)) 
        list.append(es) if (not negation) else list.append(logic.UnaryStmt(logic.UnaryStmt.NOT, es)) 
    elif 'is' in sentDict['relations'] or 'are'in sentDict['relations'] or 'am' in sentDict['relations']:
        for ent in sentDict['entities']:
            if ent in pronounList:
                index = key
            else:
                index = entities.index(ent)
            if 'knight' in sentDict['class'] or 'knights' in sentDict['class']:
                list.append(logic.KnightStmt(index)) if (not negation) else list.append(logic.UnaryStmt(logic.UnaryStmt.NOT, logic.KnightStmt(index)))
            else:
                us = logic.UnaryStmt(logic.UnaryStmt.NOT, logic.KnightStmt(index))
                list.append(us) if (not negation) else list.append(logic.UnaryStmt(logic.UnaryStmt.NOT, us))
    return list

def createBinaryFromCompound(binary_stmt, connection):
    if connection == 'or':
        return logic.BinaryStmt(binary_stmt[0], logic.BinaryStmt.OR, binary_stmt[1])
    else:
        return logic.BinaryStmt(binary_stmt[0], logic.BinaryStmt.AND, binary_stmt[1])

def isCompoundAnd(str):
    if ' and ' in str and 'and I' not in str and 'I and' not in str:
        if 'both' in str.lower():
            return True
        else:
            return False
    else:
        return False

def convertToLogic(entities, dictionary):
    list = []
    str1 = 'only a knave would say'
    str2 = 'only a knight would say'
    binary_stmt = []
    prevEntities = []
    for k in dictionary.keys():
        if str1 in dictionary[k].lower():
            dictionary[k] = 'not' + dictionary[k][(dictionary[k].find(str1) + len(str1)):]
        elif str2 in dictionary[k].lower():
            dictionary[k] = dictionary[k][(dictionary[k].find(str2) + len(str2)):]

        if 'could' in dictionary[k] or 'would' in dictionary[k] or 'tells you' in dictionary[k]:
            new_stmt = re.split('would tell you|could say|could not say|could claim|could not claim|tells you', dictionary[k])
            if 'I' in new_stmt[1]:
                new_stmt[1] = re.sub('that I am', entities[k] + ' is', new_stmt[1].strip())
            if 'I' in new_stmt[0]:
                new_stmt[0] = re.sub('I', entities[k], new_stmt[0].strip())
            sentDict = parseTree(initializeDict(), createChunkTree(new_stmt[1]))
            stmts = createLogicStmt(entities, entities.index(new_stmt[0].strip()), sentDict)
	elif ' or ' in dictionary[k] or isCompoundAnd(dictionary[k]):
            temp = dictionary[k]
            compound_stmts = re.split('or|and', dictionary[k])
            for stmt in compound_stmts:
                sentDict = parseTree(initializeDict(), createChunkTree(dictionary[k]))
                if sentDict['entities'] == [] and prevEntities != []:
                    sentDict['entities'] = prevEntities
                if 'is' not in sentDict['relations'] and 'are' not in sentDict['relations'] and 'am' not in sentDict['relations']:
                    sentDict['relations'].append('is') if (len(sentDict['entities']) == 1) else sentDict['relations'].append('are')
                for s in createLogicStmt(entities, k, sentDict):
                    binary_stmt.append(s)
                prevEntities = sentDict['entities']
            if 'or' in temp:
                stmts = [createBinaryFromCompound(binary_stmt, 'or')]
            else:
                stmts = [createBinaryFromCompound(binary_stmt, 'and')]
        else:
            sentDict = parseTree(initializeDict(), createChunkTree(dictionary[k]))
            stmts = createLogicStmt(entities, k, sentDict)
	for item in stmts:
            list.append(item)
    return list

def main():
    #entities = ['Zoey', 'Mel']
    #dict = {0: 'Mel is a knave', 1: 'Neither Zoey nor I are knaves.'}
    #entities = ['Peggy', 'Zippy']
    #dict = {0: 'of Zippy and I, exactly one is a knight', 1: 'only a knave would say that Peggy is a knave.'}
    #entities = ['Sue', 'Zippy']
    #dict = {0: 'Zippy is a knave', 1: 'I and Sue are knights.'}
    #entities = ['Sally', 'Zippy']
    #dict = {0: 'I and Zippy are not the same.', 1: 'Of I and Sally, exactly one is a knight.'}
    #entities = ['Homer', 'Bozo']
    #dict = {0: 'At least one of the following is true: that I am a knight or that Bozo is a knight.', 1: 'Homer could say that I am a knave.'}
    #entities = ['Marge', 'Zoey']
    #dict = {0: 'Zoey and I are both knights or both knaves.', 1: 'Marge and I are the same.'}
    #entities = ['Mel', 'Ted']
    #dict = {0: 'Either Ted is a knight or I am a knight.', 1: 'Ted tells you that Mel is a knave.'}
    #entities = ['Zed', 'Alice']
    #dict = {0: 'I am a knight or Alice is a knave.', 1: 'Of Zed and I, exactly one is a knight.'}
    #entities = ['Ted', 'Zeke']
    #dict = {0: 'Zeke could say that I am a knave.', 1: "it's not the case that Ted is a knave."}
    #entities = ['Ted', 'Zippy']
    #dict = {0: 'Of I and Zippy, exactly one is a knight.', 1: 'Ted is a knave.'}
    #entities = ['Zed', 'Bart']
    #dict = {0: 'Bart is a knight or I am a knight.', 1: 'Zed could claim that I am a knave.'}
    #entities = ['Bob', 'Betty']
    #dict = {0: 'Betty is a knave.', 1: 'I am a knight or Bob is a knight.'}
    #entities = ['Bart', 'Ted']
    #dict = {0: 'I and Ted are both knights or both knaves.', 1: 'Bart would tell you that I am a knave.'}
    #entities = ['Bart', 'Mel']
    #dict = {0: 'Both I am a knight and Mel is a knave.', 1: 'I would tell you that Bart is a knight.'}
    #entities = ['Betty', 'Peggy']
    #dict = {0: 'Peggy is a knave.', 1: 'Betty and I are both knights.'}
    #entities = ['Bob', 'Mel']
    #dict = {0: 'At least one of the following is true: that I am a knight or that Mel is a knave.', 1: 'Only a knave would say that Bob is a knave.'}
    #entities = ['Zed', 'Alice']
    #dict = {0: 'Alice could say that I am a knight.', 1: "It's not the case that Zed is a knave."}
    #entities = ['Alice', 'Ted']
    #dict = {0: 'Either Ted is a knave or I am a knight.', 1: 'Of I and Alice, exactly one is a knight.'}
    #entities = ['Zeke', 'Dave']
    #dict = {0: 'Of I and Dave, exactly one is a knight.', 1: 'Zeke could claim that I am a knight.'}
    #entities = ['Zed', 'Zoey']
    #dict = {0: "it's false that Zoey is a knave.", 1: 'I and Zed are different.'}
    #entities = ['Sue', 'Marge']
    #dict = {0: 'Marge is a knave.', 1: 'Sue and I are not the same.'}
    #entities = ['Bob', 'Ted']
    #dict = {0: 'I am a knight or Ted is a knave.', 1: 'only a knave would say that Bob is a knave.'}
    #entities = ['Zed', 'Peggy']
    #dict = {0: 'Peggy is a knave.', 1: 'Either Zed is a knight or I am a knight.'}
    #entities = ['Zed', 'Bob']
    #dict = {0: 'Both I am a knight and Bob is a knave.', 1: 'Zed could say that I am a knight.'}

    entities = ['Rex', 'Marge']
    dict = {0: 'I and Marge are knights.', 1: 'I would tell you that Rex is a knight.'}

    logicStmts = convertToLogic(entities, dict)
    print logicStmts

if __name__ == '__main__':
    main()
