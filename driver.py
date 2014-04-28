'''
Created on Apr 22, 2014

@author: user
'''

from Code import Code
import csv



if __name__ == '__main__':
    reader=csv.reader(open("/home/user/adm/admsolutionattempts.csv","rb"),delimiter=',')
    x = list(reader)
    
    reader=csv.reader(open("/home/user/adm/task.csv","rb"),delimiter=',')
    t = list(reader)
    
    
    code ='''
class Object:
    import                 numpy                 as                    np
    #jknlkjnlkjnljnlkj kj klj lkj ;lkj lkj l lhkhkhj kjh khkj 
    
    def               iets(b,a):
        return np.array(a==b)
        
    def ietsAnders                     (                a           )                  :
        return a
        
    numpy.array(        a           ==          b              )'''
    
    code = '''
"""Dit is een module doc."""
    
def fibonacci(number):
    #sdkjfhlsdkfjh
    #jhaldsflkashflaks
    if number < 2:
        return number
    else:
        first = 0
        second = 1
        for i in range(2,number):
            third = first + second
            first = second
            second = third
        return third

def message():
    return "The 150e Fibonacci number = " + str(fibonacci(150))
        
print message()

'''
    
    code = '''
    import numpy as np
    
    def getHashCopy(self):
        newCode = ''
        for line in self.baseMatrix:
            newCode += 'd' + 500 + int(line.deltaIndent) + ' '
            for bone in line.skel():
                md5 = md5()
                md5.update(bone)
                newCode += md5.hexdigest()[0:4] + ' '
            newCode = newCode[0:-1] + '\n'
        return newCode 
'''

    code = '''def sigsim(ss1,ss2):\n    similar=0\n    for i in range(0,len(ss1)):\n        if(ss1[i] == ss2[i]):\n            similar+=1\n    \n    return float(similar)/float(len(ss1))\n'''
    
    code = '''#===============================================================================\n# Task 5: Implement a function sigsim(ss1, ss2) which calculates the similarity of signatures ss1 and ss2.\n# Note that it doesn't matter if the signatures consist of integers (as in the case of minhashing) or of -1's\n# and +1's (as in the case of sketches) - the procedure is the same.\n#===============================================================================\n\ndef sigsim(ss1,ss2):\n    similar=0\n    for i in range(0,len(ss1)):\n        if(ss1[i] == ss2[i]):\n            similar+=1\n    \n    return float(similar)/float(len(ss1))'''
    code = code
    print code
    print "==================="
    myProgram = Code(code)
    
    print myProgram.getWorkingCopy()
    print "==================="
    print myProgram.getHashCopy()
    
    print "==================="
    fingerprint = myProgram.getWinnow(12)
    print fingerprint
    
    
        