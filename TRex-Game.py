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


## TRex-Game.py
## Software Requirements:
# ncurses library
# Python 2.7
## Syntax:  
# > py -2.7 TRex-Game.py

import curses
import logging
from time import sleep
from Scene import Ground,Cloud,Cactus
from Actors import Trex

BORDER_X,BORDER_Y = 100,30
PAD_X,PAD_Y = 2,2
NO_BORDER = 0
HORIZON = (BORDER_Y//2)
HORIZON_1BY3 = (BORDER_Y//3)
HORIZON_2BY3 = (2*BORDER_Y//3)

MESSAGE_WIN_X,MESSAGE_WIN_Y = 27,10
#score board
SCORE_X,SCORE_Y = 85,3
SCORE_BOARD_HEADER = "The T-REX Game"
SCORE_TITLE = "SCORE: "
LEVEL_TITLE = "LEVEL: "
# delays 
SHORT_DELAY = (30000/1000000.0)
DELAY = (50000/1000000.0)
LONG_DELAY = (60000/1000000.0)

# key codes 
KEY_SPACEBAR = 32
KEY_ESC = 27
KEY_ENTER =10
KEY_NONE = 0

# misc 
MAX_JUMP = 5


# game states 
GS_INIT = 1
GS_START = 2
GS_RUN = 3
GS_COLLISION = 4
GS_RESET = 5
GS_EXIT = 0
GS_ERROR = -1

isCactus = False
FREE_PLAY = 30

class Main:
    def __init__(self,window):
        global KEY_SPACEBAR,KEY_ESC,KEY_ENTER,KEY_NONE
        
        self.key_hit = KEY_NONE
        self.delay = DELAY
        self.score = 0
        self.level = 1
        self.isJump = False
        self.isCollision = False
        self.isReset = False
        self.cactus_pos = [-1,-1]
        self.trex_pos = [100,100]
        
        # init objects
        self.window = window
        self.ground = Ground(window)
        self.cloud = Cloud(window)
        self.cacti = Cactus(window)
        self.trex = Trex(window)
    
    
    def reset_game(self):
        '''
        Initializes the game state
        '''
        self.key_hit = KEY_NONE
        self.delay = DELAY
        self.score = 0
        self.level = 1
        self.isJump = False
        self.isCollision = False
        self.isReset = False
        self.cactus_pos = [-1,-1]
        self.trex_pos = [100,100]

        # init objects
        self.curse_lib = curses_lib
        self.ground = Ground(self.window)
        self.cacti = Cactus(self.window)
        self.trex = Trex(self.window)
        self.window.clear()
        
        
    def get_score(self):
        return self.score
    
    def set_score(self, score):
        self.score = score
    
    def draw_score(self):
        self.window.addstr(SCORE_Y-2,SCORE_X-3,SCORE_BOARD_HEADER)
        self.window.addstr(SCORE_Y,SCORE_X,SCORE_TITLE + str(self.score))
        self.window.addstr(SCORE_Y+1,SCORE_X, LEVEL_TITLE + str(self.level))
    
    def level_up(self):
        if (self.score%100 == 0) and self.score > 0:
            self.level = self.level + 1
            curses.beep()
        

    def end_game(self,game_state=GS_RESET):
        global GS_RESET,NO_BORDER,MESSAGE_WIN_Y,MESSAGE_WIN_X
        image_game_over =["  ___   _   __  __ ___    _____   _____ ___ "," / __| /_\ |  \/  | __|  / _ \ \ / / __| _ \\","| (_ |/ _ \| |\/| | _|  | (_) \ V /| _||   /"," \___/_/ \_\_|  |_|___|  \___/ \_/ |___|_|_\\","Press 'Enter' Key to Restart or 'ESC' to Quit"]
        self.window.clear()
        self.window.border(NO_BORDER)
        self.window.addstr(MESSAGE_WIN_Y,MESSAGE_WIN_X,     image_game_over[0])
        self.window.addstr(MESSAGE_WIN_Y+1,MESSAGE_WIN_X,   image_game_over[1])
        self.window.addstr(MESSAGE_WIN_Y+2,MESSAGE_WIN_X,   image_game_over[2])
        self.window.addstr(MESSAGE_WIN_Y+3,MESSAGE_WIN_X,   image_game_over[3])
        self.window.addstr(MESSAGE_WIN_Y+5,MESSAGE_WIN_X+15,"FINAL_SCORE : "+str(self.get_score()))
        if game_state is GS_RESET:
            self.window.addstr(MESSAGE_WIN_Y+7,MESSAGE_WIN_X+1,     image_game_over[4])

    def check_collision(self):
        if self.cactus_pos is None or self.trex_pos is None:
            return

        trex_y,trex_x = self.trex_pos[0],self.trex_pos[1]
        cactus_y,cactus_x = self.cactus_pos[0],self.cactus_pos[1]

        logging.info("trex_pos: "+str(self.trex_pos)+", cactus_pos: "+str(self.cactus_pos))
        if (cactus_x <= 16 and cactus_x >= 11) and (abs(cactus_y - trex_y) < 2):
            self.isCollision = True
            return

    
    def start(self):
        global GS_RESET,MESSAGE_WIN_Y,MESSAGE_WIN_X, isCactus

        while(self.key_hit is not KEY_ESC):
            self.window.clear()
            
            if self.isReset:
                sleep(SHORT_DELAY)
                self.isReset = False
            
            self.check_collision()

            
            self.window.border(NO_BORDER)
            # draw scene

            if self.get_score() >= FREE_PLAY:
                isCactus = True
                
            self.cactus_pos = self.ground.update(self.level,isCactus)

            self.cloud.update()
            
            self.isJump = self.trex.update(self.isJump,self.isCollision)    # jump state = False ,once the trex has completed the jump
            self.trex_pos = self.trex.get_trex_range()

            self.draw_score()
            
            key_event = window.getch()
            self.key_hit = self.key_hit if key_event == -1 else key_event
            
            if self.key_hit is KEY_SPACEBAR:
                self.isJump = True      # jump state = True on space bar hit
                self.key_hit = KEY_NONE
                
            self.set_score(self.score + 1)
            self.level_up()
            if self.isCollision:
                sleep(2)
                self.end_game(GS_RESET)
                for count in xrange(5,-1,-1):
                    self.window.addstr(MESSAGE_WIN_Y+10,MESSAGE_WIN_X+8,"Restarting in "+str(count)+" seconds!!")
                    key_event = window.getch()
                    if key_event is KEY_ESC:
                        return
                    elif key_event is KEY_ENTER:
                        self.reset_game()
                        break
                    
                    sleep(1)
                    self.window.refresh()
                self.reset_game()
                
                self.window.refresh()
                sleep(DELAY)
                
        
if __name__ == '__main__':

    # prepare game environment
    logging.basicConfig(filename='trex_game.log',level=logging.DEBUG)
    curses_lib = curses.initscr()
    window = curses.newwin(BORDER_Y,BORDER_X,0,0)
    logging.info("Init Game Window")
    curses.noecho()
    curses.curs_set(0)
    window.border(NO_BORDER)
    window.nodelay(1)

    # init game
    main_game = Main(window)
    
    # start game
    main_game.start()
    
    # clean up
    window.clear()
    main_game.end_game()
    window.refresh()
    curses.endwin()

