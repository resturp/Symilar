'''
Created on Apr 26, 2014

@author: user
'''
import unittest
from Code import Code
import csv

class Test(unittest.TestCase):


    def testEquality(self):
        assert(Code('').getWorkingCopy() == Code('#').getWorkingCopy())
        

    def testInEquality(self):
        assert(Code('').getWorkingCopy() != Code('"""I"""').getWorkingCopy())
        
    def testSelfTestHash(self):
        assert(Code('''print 'Hello world! ' + str(10) ''').getHashCopy() == \
               Code('''print 'Some other text' + str(10) ''').getHashCopy())

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEquality']
    unittest.main()