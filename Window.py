'''
Created on Apr 27, 2014

@author: user
'''
import numpy as np

class Window(object):

    def addChunk(self,chunk, linenumber):            
        self.chunks[self.pivot] = [chunk, linenumber]    
        self.pivot = (self.pivot + 1) % self.windowsize
        if self.pivot == 0:
            self.initialized = True

        if self.initialized:
            minchunk = 'g000'
            maxline = 0
            for achunk in self.chunks:
                if achunk[0] < minchunk:
                    minchunk = achunk[0]
                    maxline = achunk[1]
                else:
                    if achunk[0] == minchunk:
                        if achunk[1] > maxline:
                            maxline = achunk[1]            
            if [minchunk,maxline] != self.lastMin:
                self.fingerPrint.append([minchunk,maxline])
                self.lastMin = [minchunk,maxline]

    def __init__(self, size=5):
        self.pivot = 0
        self.windowsize = size
        self.chunks = [['',0]] * size
        self.lastMin = ['',0]
        self.fingerPrint = []
        self.initialized = False
        