'''
Solves some logic puzzle given in formal terms of Knights and Knaves

Created on Nov 12, 2012

@author: Karl
'''

class ExistsStmt:
    GT, LT, GTE, LTE, EQ = range(5)
    
    def __init__(self, op, num, stmt = True, entities = None):
        self.op = op
        self.n = num
        self.stmt = stmt
        self.ents = entities
        
    def test(self, assignment):
        def count(assn):
            count = 0
            entities = assn if self.ents == None else [assn[i] for i in self.ents] 
            for a in entities:
                if ((self.stmt == True and a) or
                    (self.stmt == False and not a) or
                    (hasattr(self.stmt, 'test') and self.stmt.test(assignment) == a)
                    ):
                        count += 1
            print assn, count
            return count
        switch = {
          ExistsStmt.GT: lambda n: count(assignment) > n,
          ExistsStmt.LT: lambda n: count(assignment) < n,
          ExistsStmt.GTE: lambda n: count(assignment) >= n,
          ExistsStmt.LTE: lambda n: count(assignment) <= n,
          ExistsStmt.EQ: lambda n: count(assignment) == n
        }
        return switch[self.op](self.n)

class BinaryStmt:
    AND, OR, IF, EQ, XOR = range(5)
    
    def __init__(self, left, op, right):
        self.l = left
        self.op = op
        self.r = right
    
    def test(self, assignment):
        switch = {
          BinaryStmt.AND: lambda x, y: x.test(assignment) and y.test(assignment),
          BinaryStmt.OR: lambda x, y: x.test(assignment) or y.test(assignment),
          BinaryStmt.IF: lambda x, y: y.test(assignment) if x.test(assignment) else True,
          BinaryStmt.EQ: lambda x, y: x.test(assignment) == y.test(assignment),
          BinaryStmt.XOR: lambda x, y: x.test(assignment) != y.test(assignment)
        }
        return switch[self.op](self.l, self.r)

class UnaryStmt:
    NOT, = range(1)
    
    def __init__(self, op, stmt):
        self.op = op
        self.s = stmt;
        
    def test(self, assignment):
        switch = {
          UnaryStmt.NOT: lambda x: not x.test(assignment)
        }
        return switch[self.op](self.s)
    
class KnightStmt:
    def __init__(self, index):
        self.i = index
    
    def test(self, assignment):
        return assignment[self.i]
    
def generateAssignments(num):
    if num == 1:
        return [[True], [False]]
    else:
        assns = generateAssignments(num - 1)
        newAssns = []
        for assn in assns:
            newAssns.append(assn + [True])
            newAssns.append(assn + [False])
        return newAssns

# Brute force!
def findSolutions(entityList, statementDict):
    assns = generateAssignments(len(entityList))
    solns = []
    for assn in assns:
        sat = True
        for k, v in statementDict.items():
            sat = sat and (assn[k] == v.test(assn))
        if sat:
            solns.append(assn)
    return solns

def main():
    entities = ['Alice', 'Bob', 'Chad']
    stmts = {0 : ExistsStmt(ExistsStmt.EQ, 1, KnightStmt(0), [0, 1, 2]),
             1 : UnaryStmt(UnaryStmt.NOT, KnightStmt(2)),
             2 : BinaryStmt(KnightStmt(0), 
                            BinaryStmt.AND,
                            KnightStmt(1))}
    solns = findSolutions(entities, stmts)
    if len(solns) == 0:
        print 'No solution found.'
    elif len(solns) > 1:
        print 'Not enough info.'
    else:
        for i in range (len(entities)):
            print entities[i], ":", "Knight" if solns[0][i] else "Knave"        

if __name__ == '__main__':
    main()
