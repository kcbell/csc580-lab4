'''
Converts statements in plain text to statements in kkLogic

Created on Nov 18, 2012

@author: Karl
'''

import re

from kkPuzzleParser import parsePuz
from kkLogic import BinaryStmt, ExistsStmt, UnaryStmt, KnightStmt, KnaveStmt

def ks(ref, string):
    return KnightStmt(ref) if string == "knight" else KnaveStmt(ref)

statements = 
    [
    ('^(\d) and (\d) is both (knight|knave) or both (knight|knave)',
    lambda x: BinaryStmt(KnightStmt(int(x[0])), BinaryStmt.EQ, KnightStmt(int(x[1])))
    ),
    ('^(\d) is (knight|knave) or (\d) is (knight|knave)',
    lambda x: BinaryStmt(ks(int(x[0]), x[1]), BinaryStmt.OR, ks(int(x[2]), x[3]))
    ),
    ('^(\d) and (\d) is (knight|knave)',
    lambda x: BinaryStmt(ks(int(x[0]), x[2]), BinaryStmt.AND, ks(int(x[1]), x[2]))
    ),
    ('^(\d) and (\d) is the same',
    lambda x: BinaryStmt(KnightStmt(int(x[0])), BinaryStmt.EQ, KnightStmt(int(x[1])))
    ),
    ('^(\d) and (\d) is both (knight|knave)',
    lambda x: BinaryStmt(ks(int(x[0]), x[2]), BinaryStmt.AND, ks(int(x[1]), x[2]))
    ),
    ('^(\d) and (\d) is different',
    lambda x: BinaryStmt(KnightStmt(int(x[0])), BinaryStmt.NEQ, KnightStmt(int(x[1])))
    ),
    ('^(\d) is (knight|knave) and (\d) is (knight|knave)',
    lambda x: BinaryStmt(ks(int(x[0]), x[1]), BinaryStmt.AND, ks(int(x[2]), x[3]))
    ),
    ('^of (\d) and (\d) exactly one is (knight|knave)',
    lambda x: ExistsStmt(ExistsStmt.EQ, 1, x[2] == "knight", [int(x[0]), int(x[1])])
    ),
    ('^neither (\d) nor (\d) is (knight|knave)',
    lambda x: BinaryStmt(UnaryStmt(UnaryStmt.NOT, ks(int(x[0]), x[2])), BinaryStmt.AND, UnaryStmt(UnaryStmt.NOT, ks(int(x[1]), x[2])))
    ),
    ('^(\d) is (knight|knave)',
    lambda x: ks(int(x[0]), x[1])
    )
    ]

def replaceEntities(entities, entity, statement):
    ret = statement.replace("1", "one").replace("2", "two") # more but they don't actually occur
    for i in xrange(len(entities)):
        if entities[i] in ret:
            ret = ret.replace(entities[i], "%d" % i)
    ret = re.sub("(\s*I\s+|\s+I[.!, ]|\s*[Mm]e\s+|\s+me[.!, ])", " %d " % entity, ret)
    return ret.strip()

def replaceRedundance(statement, entity):
    ret = statement.lower()
    ret = ret.replace("`", "")
    ret = ret.replace("'", "")
    ret = ret.replace(",", "")
    ret = ret.replace(".", "")
    ret = ret.replace("knights", "knight")
    ret = ret.replace("knaves", "knave")
    ret = re.sub("^%d know" % entity, "", ret)
    ret = re.sub("\s+(am|are|is)\s*", " is ", ret)
    ret = re.sub("\s*(am|are|is)\s+", " is ", ret)
    ret = re.sub("\s+(a|that)\s+", " ", ret)
    ret = re.sub("it\s+is", " its ", ret)
    ret = re.sub("^either\s+", "", ret)
    ret = re.sub("^both\s+", "", ret)
    ret = re.sub("(could\s+claim\s*|would\s+tell\s+you|could\s+say|would\s+say)", " says ", ret)
    ret = re.sub("(its\s+false\s*|its\s+not\s+the\s+case|its\s+not\s+true)", " its false ", ret)
    ret = re.sub("\s+", " ", ret)
    ret = re.sub("^at least one of the following is true: ", "", ret)
    ret = re.sub("is both kk or both kk", "is the same", ret)
    ret = re.sub("(not the same|different)", "different", ret)
    return ret.strip()

def parseCleanStatement(entities, entity, stmt):
    m = re.match("only (knight|knave) says (.+)", stmt)
    if m != None:
        if (m.group(1) == 'knight'):
            return parseCleanStatement(entities, entity, m.group(2))
        else:
            return UnaryStmt(UnaryStmt.NOT, parseCleanStatement(entities, entity, m.group(2).strip()))
    m = re.match("its false (.+)", stmt)
    if m != None:
        return UnaryStmt(UnaryStmt.NOT, parseCleanStatement(entities, entity, m.group(1).strip()))
    m = re.match("(\d) says (.+)", stmt)
    if m != None:
        return ExistsStmt(ExistsStmt.EQ, 1, parseCleanStatement(entities, entity, m.group(2).strip()), [int(m.group(1))])
    for regex, fun in statements:
        m = re.match(regex, stmt)
        if (m != None):
            return fun(m.groups())
    raise ValueError(stmt)

def parseStatement(entities, entity, statement):
    clean = replaceRedundance(replaceEntities(entities, entity, statement), entity)
    return parseCleanStatement(entities, entity, clean)

def parseEntities(entities, entity, phrase):
    if phrase == None:
        return set()
    ret = set()
    for e in entities:
        if e in phrase:
            ret.add(e)
    if re.search("(\s*I\s+|\s+I[.!, ]|\s*[Mm]e\s+|\s+me[.!, ])", phrase) != None:
        ret.add(entity)
    return ret

def parseStatements(entities, puzDict):
    retDict = {}
    for entity, statement in puzDict.iteritems():
        retDict[entity] = parseStatement(entities, entity, statement)
    return retDict
    
def main():
    try:
        while True:
            entities, puzDict = parsePuz(raw_input().strip().replace("`", "'"))
            print entities
            for entity, statement in puzDict.iteritems():
                parsed = parseStatement(entities, entity, statement)
                print entity, ":", statement, "->", parsed
    except EOFError:
        print

if __name__ == '__main__':
    main()
    
