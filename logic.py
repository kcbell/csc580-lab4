'''
Created on Nov 12, 2012

@author: Karl
'''

LIST = ['A', 'B']

class BinaryStmt:
    AND, OR, IF, EQ, XOR = range(5)
    
    def __init__(self, left, op, right):
        self.l = left
        self.op = op
        self.r = right
    
    def test(self, assignment):
        switch = {
          self.AND: lambda x, y: x.test(assignment) and y.test(assignment),
          self.OR: lambda x, y: x.test(assignment) or y.test(assignment),
          self.IF: lambda x, y: y.test(assignment) if x.test(assignment) else True,
          self.EQ: lambda x, y: x.test(assignment) == y.test(assignment),
          self.XOR: lambda x, y: x.test(assignment) != y.test(assignment)
        }
        return switch[self.op](self.l, self.r)

class UnaryStmt:
    NOT = range(1)
    
    def __init__(self, op, stmt):
        self.op = op
        self.s = stmt;
        
    def test(self, assignment):
        switch = {
          self.NOT: lambda x: not x.test(assignment)
        }
        return switch[self.op](self.s)
    
class ReferenceStmt:
    def __init__(self, index):
        self.i = index
    
    def test(self, assignment):
        return assignment[self.i]

def findSolution(self, entityList, statementDict):
    pass

def main():
    entities = ['A', 'B']
    stmts = {'A' : UnaryStmt(UnaryStmt.NOT, 'B'),
             'B' : BinaryStmt('A', BinaryStmt.AND, 'B')}
    soln = findSolution(entities, stmts)
    if soln == None:
        print 'No solution found.'
    else:
        for i in range (len(entities)):
            print entities[i], ":", "Knight" if soln[i] else "Knave"
            
        

if __name__ == '__main__':
    main()
