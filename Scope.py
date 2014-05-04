"""module:: symilar/Scope
:platform: Linix
:synopsis: Class for manipulating a scope within a program file.

.. moduleauthor:: Thomas Boose <thomas@boose.nl>

.. license:: Copyright 2014 Thomas Boose
thomas at boose dot nl.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import translator


class Scope(object):
    scopes = []
    methods = {}
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
        self.lastword = ''
    
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
    
    def getScopeByMethode(self, methodName):
        if methodName in self.methods.keys():
            return self.methods[methodName]
        else:
            try:
                return self.parent.getScopeByMethode(methodName)
            except:
                return getCurrentScope()
            
    def collectAllScopes(self):
        myList = [self,]
        for scope in Scope.scopes:
            if scope.parent == self:
                myList.extend(scope.collectAllScopes())
        return myList
             
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
        #print '===== translator ======'
        #print scope.antiTranslator
        #print '=== anti translator ==='

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def clearScopes(list=None):
    if list == None:
        Scope.scopes = []
    else:
        for item in list:
            try:
                Scope.scopes.remove(item)
            except:
                pass
        
        
        