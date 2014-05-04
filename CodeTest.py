'''
Created on Apr 26, 2014

@author: user
'''
import unittest
import csv
import sys

from Code import Code
from Scope import *
from cStringIO import StringIO


class Test(unittest.TestCase):


    def testEquality(self):
        assert(Code('').getWorkingCopy() == Code('#').getWorkingCopy())
        
    def testInEquality(self):
        assert(Code('').getWorkingCopy() != Code('"""I"""').getWorkingCopy())
        
    def testSelfTestHash(self):
        A = Code('''print 'Hello world! ' + str(10) ''').getHashCopy() 
        B = Code('''print 'Dit is ook een tekst! ' + str(10) ''').getHashCopy()
        assert A == B
        
    def testComplexNamingAndScopesAndNamedArguments(self):
        '''This is a complex test that tests a lot of scope handling issues.
        The getWorkingCopy() method of a Code object should return a copy of the programcode
        in which all names are replaced by generic terms. "name000x", "const000x" and "meth000x".
        
        If we create a method with def name(): we create a new scope. within this scope some names 
        can be declared. If we call this method, names used within the parentheses should be renamed
        according to the current scope. However if we use named argument, as in add(nrtwo="1") the renaming
        of "nrtwo" should occur in the scope of the called method.    
        '''
        
        A = Code('''
def add(nrone=1, nrtwo=2):
    nrtwo = float(nrtwo)
    nrone = float(nrone)
    return nrone + nrtwo
    
print add(2,3) + add (nrtwo = "1")        
''')

        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(A.getWorkingCopy())
        sys.stdout = old_stdout
        assert float(redirected_output.getvalue() ) == 7


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEquality']
    unittest.main()