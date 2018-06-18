
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

# Scene.py
from random import randint
from time import sleep
import logging

# delays 
SHORT_DELAY = (30000/1000000.0)
DELAY = (50000/1000000.0)
LONG_DELAY = (60000/1000000.0)

ground = "___________________&______.._______________;.,,,_____________________&______.._____________________"

ground_type = ["____","_&__","__;_","...."]
GROUND_FLAT = 0
GROUND_GRASS = 1
GROUND_ROCK = 2
GROUND_BROKEN = 3
NUM_GND = 4
G_Y,G_X = 20,2 

CACTI_LEVEL_0 = ["   ","# |  ","#_|_#","  |  "]
CACTI_LEVEL_1 = ["   ","#_| #","|_#  ","  |  "]
CACTI_LEVEL_2 = ["# | #","#_| #","|_#  ","  |  "]
CACTI_LEVEL_3 = ["# | #","# |_#","#_|  ","  |  "]
CACTI_LEVEL_4 = ["# |  ","# | #","#_|_#","  |  "]

CACTI_OFFSET = 96

class Cloud:
    def __init__(self,window):
        self.cloud = ["@@@","..@@@@@...."]
        self.image = ""
        self.window = window
    
    def draw(self,y,x):
        sleep(0.01)
        self.window.addstr(y,x,self.cloud[0])
        self.window.addstr(y+1,x-3,self.cloud[1])
        
    def update(self):
        n = randint(1,3)
        for count in xrange(n):
            y,x = randint(5,10),randint(30,70)
            self.draw(y,x)

class Cactus:
    def __init__(self,window):
        self.window = window
    
    def draw(self,y,x,image):
        self.window.addstr(y-3,x,   image[0])
        self.window.addstr(y-2,x,   image[1])
        self.window.addstr(y-1,x,   image[2])
        self.window.addstr(y,x,     image[3])
        
    def update(self,y,x,image):
        # set cacti level based on game level
        self.draw(y,x+CACTI_OFFSET,image)

class Ground:
    def __init__(self,window):
        global ground, ground_type
        self.ground = ground
        self.window = window
        self.cactus = []
        
    def draw(self,y,x,image):
        self.window.addstr(y,x,image)
    
    def add_cactus(self):
        self.cactus.append(Cactus(self.window))

    def update(self,level=0,isCactus=False):
        global SHORT_DELAY, NUM_GND, G_Y, G_X,CACTI_OFFSET
        # prepare ground using random ground types
        # these ground type have visual value and 
        # donot change the gameplay in any way
        image = ""
        gtype_idx = int(randint(0,NUM_GND)%NUM_GND)
        image = self.ground + ground_type[gtype_idx]
        self.ground = image[4:98]
        sleep(SHORT_DELAY)
        # draw the initial ground 
        self.draw(G_Y,G_X,self.ground)

        # Draw cactus if isCactus flag is true, 
        # this flag is set True after some gametime has elapsed
        if isCactus:
            CACTI_OFFSET = (CACTI_OFFSET- 4)
            if (CACTI_OFFSET <= 0):
                CACTI_OFFSET = 96
                
            c = [CACTI_LEVEL_0,CACTI_LEVEL_1,CACTI_LEVEL_2,CACTI_LEVEL_3,CACTI_LEVEL_4]
            self.add_cactus()
            image = c[(level%3)]
            self.cactus[0].update(20,1,image)

            return [20,1+CACTI_OFFSET]


