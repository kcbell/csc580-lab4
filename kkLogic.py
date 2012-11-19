'''
Solves some logic puzzle given in formal terms of Knights and Knaves

Created on Nov 12, 2012

@author: Karl
'''

class ExistsStmt:
    EQ, NEQ, GT, LT, GTE, LTE = range(6)
    
    # stmt = True means Knight, False means Knave, some Stmt means "would say this"
    def __init__(self, op, num, stmt = True, entities = None):
        self.op = op
        self.n = num
        self.stmt = stmt
        self.ents = entities
        
    def __str__(self):
        switch = {
          ExistsStmt.GT: ">",
          ExistsStmt.LT: "<",
          ExistsStmt.GTE: ">=",
          ExistsStmt.LTE: "<=",
          ExistsStmt.EQ: "==",
          ExistsStmt.NEQ: "!="
        }
        return "Exists %s %d %s in %s" % (switch[self.op], self.n, str(self.stmt), str(self.ents))
        
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
            return count
        switch = {
          ExistsStmt.GT: lambda n: count(assignment) > n,
          ExistsStmt.LT: lambda n: count(assignment) < n,
          ExistsStmt.GTE: lambda n: count(assignment) >= n,
          ExistsStmt.LTE: lambda n: count(assignment) <= n,
          ExistsStmt.EQ: lambda n: count(assignment) == n,
          ExistsStmt.NEQ: lambda n: count(assignment) != n
        }
        return switch[self.op](self.n)

class BinaryStmt:
    EQ, AND, OR, IF, XOR = range(5)
    NEQ = XOR
    
    def __init__(self, left, op, right):
        self.l = left
        self.op = op
        self.r = right
        
    def __str__(self):
        switch = {
          BinaryStmt.AND: "&&",
          BinaryStmt.OR: "||",
          BinaryStmt.IF: "IF",
          BinaryStmt.EQ: "==",
          BinaryStmt.XOR: "!="
        }
        return "%s %s %s" % (str(self.l), switch[self.op], str(self.r))
    
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
        
    def __str__(self):
        switch = {
          UnaryStmt.NOT: "!"
        }
        return "%s%s" % (switch[self.op], str(self.s))
        
    def test(self, assignment):
        switch = {
          UnaryStmt.NOT: lambda x: not x.test(assignment)
        }
        return switch[self.op](self.s)
    
class KnightStmt:
    def __init__(self, index):
        self.i = index
    
    def __str__(self):
        return "Knight(%d)" % self.i
    
    def test(self, assignment):
        return assignment[self.i]
    
class KnaveStmt:
    def __init__(self, index):
        self.i = index
        
    def __str__(self):
        return "Knave(%d)" % self.i
    
    def test(self, assignment):
        return not assignment[self.i]
    
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

# Solving:
# You meet nine inhabitants: Dave, Homer, Carl, Sue, Rex, Mel, Zoey, Zippy and Zeke.
# Dave says that neither Rex nor Sue are knights. 
# Homer tells you, 'Mel is a knave and I am a knight.' 
# Carl says, 'Neither Zippy nor Zeke are knaves.' 
# Sue tells you that it's false that Carl is a knave. 
# Rex claims, 'Zippy and I are the same.' 
# Mel tells you that Sue and Carl are both knights or both knaves. 
# Zoey claims that Sue is a knave. 
# Zippy tells you, 'Of Sue and Dave, exactly one is a knight.' 
# Zeke claims that either Zippy is a knave or Mel is a knave.
def main():
    #            0       1        2       3      4      5      6       7        8
    entities = ['Dave', 'Homer', 'Carl', 'Sue', 'Rex', 'Mel', 'Zoey', 'Zippy', 'Zeke']
    stmts = {0: UnaryStmt(UnaryStmt.NOT, 
                          BinaryStmt(KnightStmt(4), BinaryStmt.OR, KnightStmt(3))),
             1: BinaryStmt(KnaveStmt(5), 
                           BinaryStmt.AND,
                           KnightStmt(1)),
             2: UnaryStmt(UnaryStmt.NOT, 
                          BinaryStmt(KnaveStmt(7), BinaryStmt.OR, KnaveStmt(8))),
             3: UnaryStmt(UnaryStmt.NOT, KnaveStmt(2)),
             4: BinaryStmt(KnightStmt(7), BinaryStmt.EQ, KnightStmt(4)),
             5: BinaryStmt(KnightStmt(2), BinaryStmt.EQ, KnightStmt(3)),
             6: KnaveStmt(3),
             7: ExistsStmt(ExistsStmt.EQ, 1, True, [3, 0]),
             8: BinaryStmt(KnaveStmt(7), BinaryStmt.OR, KnaveStmt(5))
             }
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
