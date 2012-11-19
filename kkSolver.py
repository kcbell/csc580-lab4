'''
Created on Nov 18, 2012

@author: Karl
'''

import sys

from kkPuzzleParser import parsePuz
from kkStatementParser import parseStatements
from kkLogic import findSolutions

def getSolns(puz):
    entities, puzDict = parsePuz(puz.strip().replace("`", "'"))
    logicDict = parseStatements(entities, puzDict)
    solns = findSolutions(entities, logicDict)
    return (entities, solns)

def main():
    args = sys.argv
    files = []
    if len(args) == 1:
        files.append(sys.stdin.read())
    else:
        if (args[1] == '-c'):
            if len(args) == 2:
                files.extend(sys.stdin.read().splitlines())
            else:
                for arg in args[2:]:
                    files.extend(open(arg, "r").read().splitlines())
        else:
            files.extend([open(arg, "r").read() for arg in args[1:]])
    
    for f in files:
        entities, solns = getSolns(f)
        if len(solns) == 0:
            print 'No solution.'
        elif len(solns) > 1:
            print 'Not enough info.'
        else:
            for i in range (len(entities)):
                print entities[i], ":", "Knight" if solns[0][i] else "Knave"
        print

if __name__ == '__main__':
    main()