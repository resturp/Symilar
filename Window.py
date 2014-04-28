"""module:: symilar/Window
:platform: Linix
:synopsis: Class for a sliding window over a string population winnow array.

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

import numpy as np

class Window(object):

    def addChunk(self,chunk, linenumber):            
        self.chunks[self.pivot] = [chunk, linenumber]    
        self.pivot = (self.pivot + 1) % self.windowsize
        self.chunkcounter += 1
        
        if self.pivot == 0:
            self.initialized = True

        if self.initialized and self.chunkcounter % self.noise == 0:
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

    def __init__(self, guarantee=5, noise=1):
        self.pivot = 0
        self.noise = noise
        self.guarantee = guarantee
        self.windowsize = guarantee - noise + 1
        self.chunks = [['',0]] * self.windowsize
        self.lastMin = ['',0]
        self.fingerPrint = []
        self.chunkcounter = 0
        self.initialized = False
        