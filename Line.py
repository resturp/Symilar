from Scope import *
import re

class Line(object):

    def updateAllTranslators(self,word, value):

        if self.nextParent:
            scope = self.scope.parent
        else:
            scope = self.scope
         
        if word == value:
            translator = scope.antiTranslator
        else:
            translator = scope.translator
             
        translator[word] = value
        self.allTranslators[word] = value
        
    def updateTranslator(self):
        '''replace all names in this line by the names in the scope'''
        #return only the line of code
        preservenext = False
        loadTranslator = False
        self.nextParent = False
        lastword = ''
        replaceNextBy = ''
        #this should not be done for each line but once, maybe per scopechange?
        self.allTranslators = self.scope.getAllTranslators()
        #print self.allTranslators.keys() 
        self.skel = []   
        pivot = 0         
        for word in re.findall(r"[\w]+", self.line):
            #append symbols to skeleton
            for bone in self.line[pivot:self.line.find(word,pivot)]:
                if not bone in [' ','\t','\n']:
                    self.skel.append(bone)
                pivot +=1
            pivot += len(word)
            #=======================
            
            if replaceNextBy != '':
                if not word in self.scope.translator.keys():
                    self.updateAllTranslators(word, replaceNextBy)
                replaceNextBy = ''
            if word in translator.getKeywords().keys():
                preservenext = False
            if word in ["from", "with", "import"]:
                if not preservenext:
                    preservenext = True
                    loadTranslator = True
            if word == "as":
                replaceNextBy = lastword
            if word in ['def', 'class']:
                self.nextParent = True
            if preservenext:
                if not word in self.allTranslators.keys():
                    self.updateAllTranslators(word, word)
                    if loadTranslator:
                        try:
                            moduleDict = translator.createModuleDict(word)
                            self.scope.antiTranslator.update(moduleDict)
                            self.allTranslators.update(moduleDict)
                        except:
                            pass
                        loadTranslator = False
            else:
                if not word in self.allTranslators.keys():
                    try:
                        if re.match(r"const[0-9]{4}", word):
                            self.updateAllTranslators(word, word)
                        else:
                            iets = float(word)
                            self.updateAllTranslators(word, word)
                    except:
                        if self.nextParent:
                            #! actually methods, classes and vars should have independant counters
                            self.updateAllTranslators(word, 'meth' + ('00000' + str(self.scope.parent.varCount))[-5:])
                            self.scope.parent.varCount += 1
                            self.nextParent = False
                        else:
                            self.updateAllTranslators(word, 'name' + ('00000' + str(self.scope.varCount))[-5:])
                            self.scope.varCount += 1
            lastword = word
            #append translated word to skeleton
            if word in self.scope.getScopeTranslators().keys():
                self.skel.append(self.scope.getScopeTranslators()[word])
            else:
                self.skel.append(word)
        #append trailing symbols to skeleton
        for bone in self.line[pivot:]:
            if not bone in [' ','\t','\n']:
                self.skel.append(bone)
            pivot +=1

    
    def replaceStringLiterals(self):    
                    
        toReturn = ''
        for quote in ['"""',"'''",'"','"']:
            quoteCount = 0
            for part in self.line.split(quote):
                if len(part) == 9 and re.match(r"const[0-9]{4}", part):
                    toReturn += '"' + part + '"'
                else:    
                    if quoteCount % 2 == 0:
                        toReturn += part 
                    else:
                        if part in self.scope.translator.keys():
                            toReturn +=  self.scope.translator[part] 
                        else:
                            self.scope.constCount += 1
                            constname = '"const' + ('0000' + str(self.scope.constCount))[-4:] + '"'
                            self.scope.translator[part] = constname 
                            toReturn += constname
                quoteCount += 1
            self.line = toReturn
            toReturn = ''
            
    
    def updateOrCreateScope(self):
        indentLevel(self.indent)
        if self.line[0:self.line.find(' ')] in ['def', 'class']:
            self.scope = Scope(self.indent)
        else:
            self.scope = getCurrentScope()
    
    def removeComment(self):
        pos = self.line.find('#')
        if pos >= 0:
            self.line = self.line[0:pos]

    def setDeltaIndent(self, lastIndent):
        self.deltaIndent = self.indent - lastIndent     

    
    def trailingTabsToSpace(self):
        try:
            while self.line[0] in [' ', '\t']:
                if self.line[0] == '\t':
                    self.line = self.line [1:]
                else:
                    self.line = self.line [4:]
                self.indent += 1
        except IndexError:
            pass

    def __init__(self, line):
        collon = line.find(':')
        self.lineNumber = int(line[0:collon])
        self.line = line[collon + 1:]
        self.indent = 0 
        self.deltaIndent = 0
        self.removeComment()
        self.trailingTabsToSpace()
        self.line = self.line.strip()
        self.allTranslators = {}
        
        if self.line != '':
            self.updateOrCreateScope()
            self.replaceStringLiterals()
            self.updateTranslator()
            
            for key in self.scope.getScopeTranslators():
                self.line = re.sub(r'\b%s\b' % key, ' ' + self.allTranslators[key] + ' ', self.line)
            lenLine = len(self.line)
            self.line = self.line.replace('  ',' ')
            while len(self.line) < lenLine:
                lenLine = len(self.line)
                self.line = self.line.replace('  ',' ')
            for char in ':,.(){}[]+-*/&|%!=':
                self.line = self.line.replace(' ' + char, char)
                self.line = self.line.replace(char + ' ', char)
            self.line = self.line.strip()
                
                
                
            

