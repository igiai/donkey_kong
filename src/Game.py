import pyxel
from random import randint
from constants import *
from Objects import *

class Game:

    def __init__(self):

        #Create the game window
        pyxel.init(WIDTH, HEIGHT, caption=CAPTION)
        # Load the pyxres file
        pyxel.load("../assets/my_resource.pyxres")

        #Lists for platforms, ladders and barrels
        self.__platforms = []
        self.__ladders = []
        self.__barrels = []

        #First platform
        self.__platforms.append(Platform(5,245,27))
        #Middle platforms
        for i in range(5):
            self.__platforms.append(Platform((i%2)*21+5, 214-i*31, 24))
        #Last platform
        self.__platforms.append(Platform(90, 59, 6))

        #Ladders
        self.__ladders.append(Ladder(85, 239, True))
        self.__ladders.append(Ladder(150, 239, False))
        self.__ladders.append(Ladder(45, 208, False))
        self.__ladders.append(Ladder(120, 208, False))
        self.__ladders.append(Ladder(68, 177, True))
        self.__ladders.append(Ladder(100, 177, False))
        self.__ladders.append(Ladder(160, 177, False))
        self.__ladders.append(Ladder(30, 146, False))
        self.__ladders.append(Ladder(75, 146, False))
        self.__ladders.append(Ladder(127, 146, True))
        self.__ladders.append(Ladder(90, 115, True))
        self.__ladders.append(Ladder(140, 115, False))
        self.__ladders.append(Ladder(122, 84, False))
        self.__ladders.append(Ladder(140, 115, False))
        self.__ladders.append(Ladder(122, 84, False))

        #Mario
        self.__mario = Mario(MARIO_X,MARIO_Y)

        #Donkey Kong
        self.__donkeyKong = DonkeyKong(DK_X, DK_Y)

        #Pauline
        self.__pauline = Pauline(PAULINE_X, PAULINE_Y)

        #Run game
        pyxel.run(self.update, self.draw)

    #Function for calculations needed every frame
    def update(self):
        #Esc to quit game
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        #Mario movements
        if pyxel.btn(pyxel.KEY_RIGHT):
            for i in self.__platforms:
                if self.__mario.x <= 182 and self.__mario.y == i.y-15:           #rigth border condition
                    self.__mario.move_right()
        if pyxel.btn(pyxel.KEY_LEFT):
            for i in self.__platforms:
                if self.__mario.y == 230:               #additional condition for the first platform
                    if self.__mario.x >= 24 and self.__mario.y == i.y-15:            #fire border condition
                        self.__mario.move_left()
                else:
                    if self.__mario.x >= 5 and self.__mario.y == i.y-15:             #left border condition
                        self.__mario.move_left()
        if pyxel.btn(pyxel.KEY_UP):
            for i in self.__ladders:
                if (self.__mario.x >= i.x-7  and self.__mario.x <= i.x+2 and self.__mario.y <= i.y-9 and self.__mario.y >= i.y-39 and i.broken == False):
                    self.__mario.move_up()
        if pyxel.btn(pyxel.KEY_DOWN):
            for i in self.__ladders:
                if (self.__mario.x >= i.x-7  and self.__mario.x <= i.x+2 and self.__mario.y >= i.y-40 and self.__mario.y <= i.y-10 and i.broken == False):
                    self.__mario.move_down()

        #Mario falls
        for i in self.__platforms:
            if self.__mario.x >= i.endRight and self.__mario.y <= i.y+15 and self.__mario.y >= i.y-33:
                self.__mario.fall()
            elif self.__mario.x <= i.endLeft-12 and self.__mario.y <= i.y+15 and self.__mario.y >= i.y-33:
                self.__mario.fall()

        #Create barrels
        if pyxel.frame_count % randint(60,100) == 0 and len(self.__barrels) < 10:
            self.__barrels.append(Barrel(BARREL_X, BARREL_Y))

        #Barrels movements
        for b in self.__barrels:
            for i in range(len(self.__platforms)-1):
                if b.y in [203, 141, 79] and b.x <= self.__platforms[i].endRight:
                    b.move_right()
                    b.toRight = True
                    b.toLeft = False
                elif (b.x >= self.__platforms[i].endRight or b.x <= self.__platforms[i].endLeft-12) and b.y <= self.__platforms[i].y+19 and b.y >= self.__platforms[i].y-33:
                    b.fall()
                elif b.y in [234, 172, 110] and b.x >= self.__platforms[i].endLeft:
                    b.move_left()
                    b.toRight = False
                    b.toLeft = True
            if pyxel.frame_count % 3 == 0:
                if b.toRight:
                    b.rotateRight()
                elif b.toLeft:
                    b.rotateLeft()

        #Barrels falls
        for b in self.__barrels:
            for i in self.__ladders:
                if (b.x >= i.x-7  and b.x <= i.x+2 and b.y >= i.y-40 and b.y <= i.y-6 and b.prob == i.prob):
                        b.fall()

        if self.__barrels[0].y == 234 and self.__barrels[0].x <= 24:
            self.__barrels.pop(0)

    #Function for drawing things on the screen
    def draw(self):
        #Background - black(0)
        pyxel.cls(0)

        #Draw platforms
        for i in self.__platforms:
            for j in range(i.length):
                pyxel.blt(i.x+j*7, i.y, 0, 0, 8, 7, 7)

        #Draw ladders
        for i in self.__ladders:
            if i.broken:
                pyxel.blt(i.x, i.y, 0, 0, 18, 8, 6, colkey=0)
                pyxel.blt(i.x, i.y-18, 0, 0, 18, 8, 6, colkey=0)
            else:
                for j in range(4):
                    pyxel.blt(i.x, i.y-6*j, 0, 0, 18, 8, 6, colkey=0)

        #Draw fire
        pyxel.blt(7, 232, 0, 8, 2, 15, 13)
        pyxel.blt(8, 222, 0, 24, 4, 15, 10)

        #Draw pauline
        pyxel.blt(self.__pauline.x, self.__pauline.y, 0, 6, 179, 15, 22)

        #Draw static barrels
        pyxel.blt(7, 73, 0, 12, 102, 10, 17)
        pyxel.blt(18, 73, 0, 12, 102, 10, 17)
        pyxel.blt(7, 57, 0, 12, 102, 10, 17)
        pyxel.blt(18, 57, 0, 12, 102, 10, 17)

        #Draw donkey king
        pyxel.blt(self.__donkeyKong.x, self.__donkeyKong.y, 0, 5, 57, 40, 33)

        #Draw bonus box
        pyxel.blt(150, 10, 0, 181, 99, 43, 20)
        score = 2054
        pyxel.text(164, 20, str(score), 7)

        #Draw lives
        pyxel.blt(8, 10, 0, 131, 8, 7, 7)
        pyxel.blt(17, 10, 0, 131, 8, 7, 7)
        pyxel.blt(26, 10, 0, 131, 8, 7, 7)

        #Draw Barrels
        for i in self.__barrels:
            if i.states["upLeft"]:
                pyxel.blt(i.x, i.y, 0, 35, 105, 12, 11, colkey=0)
            elif i.states["upRight"]:
                pyxel.blt(i.x, i.y, 0, 59, 105, 12, 11, colkey=0)
            elif i.states["downRight"]:
                pyxel.blt(i.x, i.y, 0, 83, 105, 12, 11, colkey=0)
            elif i.states["downLeft"]:
                pyxel.blt(i.x, i.y, 0, 107, 105, 12, 11, colkey=0)


        #Draw mario
        if self.__mario.states["toLeft"] == True:
            pyxel.blt(self.__mario.x, self.__mario.y, 0, 6, 32, 12, 15, colkey=0)
        if self.__mario.states["toRight"] == True:
            pyxel.blt(self.__mario.x, self.__mario.y, 0, 6, 32, -12, 15, colkey=0)
        if self.__mario.states["toBack"]:
            pyxel.blt(self.__mario.x, self.__mario.y, 0, 148, 33, 16, 15, colkey=0)
        # we use pyxel.frame_count to do things every frame (here changing color)
        # pyxel.text(0, 10, "Changing color every frame", pyxel.frame_count % 16)
        # this is done every frame... moving a text until it reaches the end
        # we can know the width and height of the screen using pyxel.width or
        # pyxel.height
        # x = pyxel.frame_count % pyxel.width
        # pyxel.text(x, 20, "Moving text", 3)
        # y = pyxel.frame_count % pyxel.height
        # pyxel.text(50, y, "Moving supertext", pyxel.frame_count % 16)
