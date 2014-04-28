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
        
        
        