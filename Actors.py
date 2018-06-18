'''
Copyright 2018 Harshdeep Sokhey

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Actors.py
from random import randint
from time import sleep
import logging

# delays 
SHORT_DELAY = (30000/1000000.0)
DELAY = (50000/1000000.0)
LONG_DELAY = (60000/1000000.0)

toggle = True
TREX = ["   =o===","   ==www",", |||-","\||||","  / \\","  \ /"]
TREX_DEAD_0 = "   =X==="
TREX_JUMP_4 = "  L L"


count = 0
class Trex:
    def __init__(self,window,):
        self.window = window
        self.image = []
        self.jump_state = False
        self.y = 20
        self.x = 4
        self.count = 0
        
    def get_trex_range(self):
        return [self.y,(self.x + 6)]

    def draw(self):
        self.window.addstr(self.y-4,self.x,self.image[0])
        self.window.addstr(self.y-3,self.x,self.image[1])
        self.window.addstr(self.y-2,self.x,self.image[2])
        self.window.addstr(self.y-1,self.x,self.image[3])
        self.window.addstr(self.y ,self.x,self.image[4])
    
    def update(self,isJump=False,isCollison=False):
        global TREX,toggle,SHORT_DELAY,LONG_DELAY,count
        self.image = TREX[:5]
        toggle = not(toggle)
        sleep(LONG_DELAY)
        if isCollison:
            self.image[0] = TREX_DEAD_0

        if not isJump:
            self.image[4] = TREX[5] if toggle else TREX[4]
        else:
            self.jump_state = True
            jmp = [-1,-2,-3,0,1,2,3]
            self.image[4] = TREX_JUMP_4
            self.y = self.y + jmp[self.count]
            self.count = (self.count + 1)%len(jmp)
            
            if self.y >= 20:
                self.y = 20 
                self.jump_state = False

        self.draw()
        
        return self.jump_state
