import translator


class Scope(object):
    scopes = []
    current = None
    classInit = True
        
    def __init__(self, indent):
        Scope.scopes.append(self)
        self.parent = getCurrentScope()
        Scope.current = self
        self.indent = indent
        self.varCount = 0
        self.translator = {}
        self.antiTranslator = {}
        self.constCount = 0
    
    def getAllTranslators(self):
        if self.indent == -1:
            myTranslator = dict(self.translator)
            myTranslator.update(self.antiTranslator)
            return myTranslator
        else:
            myTranslator = self.parent.getAllTranslators()
            myTranslator.update(self.translator)
            myTranslator.update(self.antiTranslator)
            return myTranslator
        
    def getScopeTranslators(self):
        if self.indent == -1:
            return dict(self.translator)
        else:
            myTranslator = self.parent.getScopeTranslators()
            myTranslator.update(self.translator)
            return myTranslator
        
# def __rootScopeInit():
#     if Scope.classInit:
#         Scope.classInit = False
#         Scope.scopes = []
#         Scope.current = None
    
        
def indentLevel(newIndent):
    #__rootScopeInit()
#     if newIndent == -1:
#         Scope.current = Scope.root
#     else:
    if newIndent < 0:
        newIndent = 0
    while newIndent <= Scope.current.indent:
        Scope.current = Scope.current.parent
            #Scope.getAllTranslators(Scope.current)

        
def getCurrentScope():
    return Scope.current


def printScopes():
    for scope in Scope.scopes:
        print scope.translator

def clearScopes():
    Scope.scopes = []
        
        
        