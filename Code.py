"""module:: symilar/Code
:platform: Linix
:synopsis: Class for manipulating a program file.

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

from Line import Line
from Window import Window
from Scope import *
from hashlib import md5

class Code():
    
    def createBaseMatrix(self):     
        self.rootScope = Scope(-1)
        indentLevel(-1)
        self.rootScope.antiTranslator = translator.getBuiltInNames()
        self.rootScope.antiTranslator.update(translator.getKeywords())
        
        self.baseMatrix = []
        lastIndent = 0
        #print self.code
        for part in self.code.split('~'):
            for line in part.splitlines(1):
                thisLine = Line(line)
                
                if thisLine.line != '': 
                    thisLine.setDeltaIndent(lastIndent)
                    lastIndent = thisLine.indent             
                    self.baseMatrix.append(thisLine) 
    
    def replaceMultiLineFromCode(self,quote):
        quoteCount = 0
        toReturn = ''
        for part in self.code.split(quote):
            if quoteCount % 2 == 0:
                toReturn += part
            else:
                toReturn += quote + part.replace('\n', '~').replace('/n','~') + quote
                
            quoteCount += 1
        self.code = toReturn

    def addLineNumbers(self):
        newCode = '' 
        number = 1
        for line in self.code.splitlines(1):
            newCode += str(number) + ":" + line
            number += 1
        self.code = newCode  
    
        
    
    def corectMultiLineLiterals(self):
        self.replaceMultiLineFromCode('"""')
        self.replaceMultiLineFromCode("'''")
        self.replaceMultiLineFromCode('"')
        self.replaceMultiLineFromCode("'")
        

    def getWorkingCopy(self):
        newCode = ''
        aline = False
        for line in self.baseMatrix:
            newCode += '    ' * line.indent + line.line + "\n"
            aline = True
        if aline:
            return newCode[0:-1]
        else:
            return newCode
        
    def getHashCopy(self,salt=''):
        '''Return a string representation of the code.
        
        The hash will contain chunks of 4 characters representing a
            delta-indentation, constant, name or symbol.
            
        The hash will start with a line number 'lddddddd' where d is a digit.
        The next chunck will indicate the delta of indentation.
        md5(i500) means that the indentation has not changed.
            md5(i501) means 1 indentation md5(i498) means 2 indentations back 
        '''
        newCode = ''
        for line in self.baseMatrix:
            m = md5()
            m.update('i' + str(line.deltaIndent) + salt)
            newCode += 'l' + ('0000000' + str(line.lineNumber))[-7:] +  ' ' + m.hexdigest()[0:4] + ' '
            for bone in line.skel:
                m = md5()
                m.update(bone + salt)
                newCode += m.hexdigest()[0:4] + ' '
            newCode = newCode[0:-1] + '\n'
        return newCode 
    
    
    
    def getWinnow(self, guarantee, noise=1, salt=''):
        thisWindow = Window(guarantee, noise)
        for line in self.getHashCopy(salt=salt).split('\n'):
            if line.strip() != '':
                
                lineNumber = int(line[1:line.find(' ')])
                line = line[line.find(' ') + 1:]
                for chunk in line.split(' '):
                    thisWindow.addChunk(chunk, lineNumber)
        return thisWindow.fingerPrint   
    
    def winnow2dict(self, guarantee, noise=1, salt=''):
        toReturn = []
        for [chunk,line] in self.getWinnow(guarantee, noise, salt=salt):       
            toReturn.append(chunk)
        return toReturn

    def winnow2str(self, guarantee, noise=1, salt=''):
        toReturn = ''
        for [chunk,line] in self.getWinnow(guarantee, noise, salt=salt):       
            toReturn += chunk + ' '
        return toReturn
        
    def __init__(self, code):
        self.code = code
        self.rootScope = None
        self.original = code
        self.baseMatrix = []
        self.addLineNumbers()
        self.corectMultiLineLiterals()
        self.createBaseMatrix()

        

    def __del__(self):
        myList = self.rootScope.collectAllScopes()
        clearScopes(myList)
