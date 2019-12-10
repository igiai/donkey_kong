import pyxel
from random import randint
from constants import *
from Objects import *

class Game:

    def __init__(self):
        """
        Class constructor
        Creates all game's objects except for barrels
        """
        #Create the game window
        pyxel.init(WIDTH, HEIGHT, caption=CAPTION)
        #Load the pyxres file
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

    def update(self):
        """
        Function for calculations needed every frame
        Randomly creates barrels
        """
        if pyxel.btnp(pyxel.KEY_ESCAPE):                                        #Esc to quit game
            pyxel.quit()


        for pl in self.__platforms:
            """
            Mario horizontal movements
            Right movement allowed only when Mario's x coordinate within borders
            and y coordinate appropriate for given platform
            Left movement allowed only when Mario's x coordinate within borders
            and y coordinate appropriate for given platform, on the first platform
            diferent border due to barrel with fire
            """
            if pyxel.btn(pyxel.KEY_RIGHT):
                if (self.__mario.x <= RIGHT_BORDER and                          #rigth border condition
                self.__mario.y == pl.y-MARIO_HEIGHT):                           #given plaform y coordinate condition
                    self.__mario.move_right()
            elif pyxel.btn(pyxel.KEY_LEFT):
                if self.__mario.y == 230:                                       #if mario on the first platform
                    if (self.__mario.x >= LEFT_BORDER+FIRE_WIDTH and            #left border with fire condition
                    self.__mario.y == pl.y-MARIO_HEIGHT):                       #given plaform y coordinate condition
                        self.__mario.move_left()
                else:                                                           #other platforms
                    if (self.__mario.x >= LEFT_BORDER and
                    self.__mario.y == pl.y-MARIO_HEIGHT):
                        self.__mario.move_left()
            """
            Mario falls
            Fall happen when Mario gets to the end of platform
            Fall movement lasts untill Mario's y coordinate value
            reaches platform below
            To prevent him from falling to low he can fall only when he is not
            in jump movement
            Right and left movements are allowed while in fall
            """
            if (self.__mario.x >= pl.endRight and not                           #end of platform on right condition
            self.__mario.states["inJump"] and self.__mario.y <= pl.y+15 and     #not in jump conditions and y coordinate conditions
            self.__mario.y >= pl.y-33):
                self.__mario.fall()
                if pyxel.btn(pyxel.KEY_RIGHT):
                    self.__mario.move_right()
                elif (pyxel.btn(pyxel.KEY_LEFT) and
                self.__mario.x >= pl.endRight+1):                               #left movement allowed only to endRight coordinate
                    self.__mario.move_left()
            elif (self.__mario.x <= pl.endLeft-12 and not                       #end of platform on left condition
            self.__mario.states["inJump"] and self.__mario.y <= pl.y+15 and     #not in jump conditions and y coordinate conditions
            self.__mario.y >= pl.y-33):
                self.__mario.fall()
                if (pyxel.btn(pyxel.KEY_RIGHT) and
                self.__mario.x <= pl.endLeft-13):                               #right movement allowed only to endLeft coordinate
                    self.__mario.move_right()
                elif pyxel.btn(pyxel.KEY_LEFT):
                    self.__mario.move_left()

        """
        Mario vertical movements
        Up movement allowed only when Mario's x coordinate within range of
        one of the ladders width, y coordinate within range of one of the
        ladders height, ladder is not broken and mario is not jumping
        Down movement under the same conditions and up movement
        """
        for ld in self.__ladders:
            if pyxel.btn(pyxel.KEY_UP):
                if (self.__mario.x >= ld.x-7 and self.__mario.x <= ld.x+2 and   #ladder's width range conditions
                self.__mario.y <= ld.y-9 and self.__mario.y >= ld.y-39 and      #ladder's height range conditions
                ld.broken == False and not self.__mario.states["inJump"]):
                    self.__mario.move_up()
            elif pyxel.btn(pyxel.KEY_DOWN):
                if (self.__mario.x >= ld.x-7 and self.__mario.x <= ld.x+2 and
                self.__mario.y >= ld.y-40 and self.__mario.y <= ld.y-10 and
                ld.broken == False and not self.__mario.states["inJump"]):
                    self.__mario.move_down()

        """
        Mario jump
        Jump movement when Space once pressed => inJump is set
        Right and left movements are allowed while in jump
        Jumps allowed only on platforms
        """
        if (pyxel.btn(pyxel.KEY_SPACE) and
        self.__mario.y in MARIO_PLATFORMS):                                     #jumps only on platforms condition
            self.__mario.states["inJump"] = True

        if (self.__mario.states["inJump"] == True and not
        self.__mario.states["isUp"]):                                           #ascend (jumpUp) until top (isUp)
            self.__mario.jumpUp()
            if pyxel.btn(pyxel.KEY_RIGHT):                                      #left and right movements allowed while in jumpUp
                    self.__mario.move_right()
            elif pyxel.btn(pyxel.KEY_LEFT):
                    self.__mario.move_left()
        elif self.__mario.states["isUp"]:                                       #descend (jumpDown) until bottom (not isUp)
            self.__mario.jumpDown()
            if pyxel.btn(pyxel.KEY_LEFT):                                       #left and right movements allowed while in jumpDown
                self.__mario.move_left()
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.__mario.move_right()


        """
        Create barrels
        Randomly create barrels, allow only 10 barrels at the same time
        Call grab method to animate Donkey Kong movemets
        Create and grab only allowed when Donkey Kong in normal state
        """
        if (pyxel.frame_count % randint(60,100) == 0 and
        len(self.__barrels) < 10 and self.__donkeyKong.states["normal"]):
            self.__donkeyKong.states["inGrab"] = True                           #if conditions are met, start DonkeyKong's grabing animation

        if self.__donkeyKong.states["inGrab"]:
            self.__donkeyKong.grab()

            if self.__donkeyKong.movementTime == 5:
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

        # if len(self.__barrels) > 0:
        #     for i in range(len(self.__barrels)):
        #         if self.__barrels[i].y == 234 and self.__barrels[i].x <= 24:
        #             self.__barrels.pop(i)

        if len(self.__barrels) > 0 and self.__barrels[0].y == 234 and self.__barrels[0].x <= 24:
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
        if self.__donkeyKong.states["normal"]:
            pyxel.blt(self.__donkeyKong.x, self.__donkeyKong.y, 0, 5, 57, 40, 33)
        elif self.__donkeyKong.states["toLeft"]:
            pyxel.blt(self.__donkeyKong.x, self.__donkeyKong.y, 0, 53, 58, 43, 32)
        elif self.__donkeyKong.states["withBarrel"]:
            pyxel.blt(self.__donkeyKong.x, self.__donkeyKong.y, 0, 104, 58, 40, 32)
        elif self.__donkeyKong.states["toRight"]:
            pyxel.blt(self.__donkeyKong.x, self.__donkeyKong.y, 0, 53, 58, -43, 32)

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
