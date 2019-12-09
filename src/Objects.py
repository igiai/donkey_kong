from random import randint

class Object:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = x
    @y.setter
    def y(self, y):
        self.__y = y


class Platform(Object):
    def __init__(self, x, y, length):
        super().__init__(x,y)
        self.__length = length
        self.__endLeft = x
        self.__endRight = x+7*length

    @property
    def length(self):
        return self.__length

    @property
    def endLeft(self):
        return self.__endLeft

    @property
    def endRight(self):
        return self.__endRight


class Ladder(Object):
    def __init__(self, x, y, broken):
        super().__init__(x,y)
        self.__broken = broken
        self.__prob = randint(1,4)

    @property
    def broken(self):
        return self.__broken
    @property
    def prob(self):
        return self.__prob


class DonkeyKong(Object):

    def __init__(self, x, y):
        super().__init__(x,y)
        self.__states = {"normal": True, "toRight": False, "toLeft": False, "withBarrel": False}
        self.__inGrab = 30


    def grab(self):
        if self.__inGrab > 20:
            self.__states["normal"] = False
            self.__states["toLeft"] = True
            self.__inGrab -= 1
        elif self.__inGrab <= 20 and self.__inGrab > 10:
            self.__states["toLeft"] = False
            self.__states["withBarrel"] = True
            self.__inGrab -= 1
        elif self.__inGrab <= 10 and self.__inGrab > 0:
            self.__states["withBarrel"] = False
            self.__states["toRight"] = True
            self.__inGrab -= 1
        else:
            self.__states["toRight"] = False
            self.__states["normal"] = True
            self.__inGrab = 30

    @property
    def states(self):
        return self.__states
    @property
    def inGrab(self):
        return self.__inGrab
    @states.setter
    def states(self, states):
        self.__states = states


class Pauline(Object):
    def __init__(self, x, y):
        super().__init__(x,y)


class Barrel(Object):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.__prob = randint(1,4)
        self.__states = {"upLeft": True, "upRight": False, "downRight": False, "downLeft": False}
        self.__toRight = True
        self.__toleft = False

    def move_right(self):
        self.x = self.x + 0.25

    def move_left(self):
        self.x = self.x - 0.25

    def fall(self):
        self.y = self.y + 1

    def rotateRight(self):
        if self.__states["upLeft"] == True:
            self.__states["upRight"] = True
            self.__states["upLeft"] = False
        elif self.__states["upRight"] == True:
            self.__states["downRight"] = True
            self.__states["upRight"] = False
        elif self.__states["downRight"] == True:
            self.__states["downLeft"] = True
            self.__states["downRight"] = False
        elif self.__states["downLeft"] == True:
            self.__states["upLeft"] = True
            self.__states["downLeft"] = False

    def rotateLeft(self):
        if self.__states["upLeft"] == True:
            self.__states["upLeft"] = False
            self.__states["downLeft"] = True
        elif self.__states["downLeft"] == True:
            self.__states["downRight"] = True
            self.__states["downLeft"] = False
        elif self.__states["downRight"] == True:
            self.__states["upRight"] = True
            self.__states["downRight"] = False
        elif self.__states["upRight"] == True:
            self.__states["upLeft"] = True
            self.__states["upRight"] = False


    @property
    def prob(self):
        return self.__prob
    @property
    def states(self):
        return self.__states
    @property
    def toRight(self):
        return self.__toRight
    @property
    def toLeft(self):
        return self.__toleft
    @toRight.setter
    def toRight(self, toRight):
        self.__toRight = toRight
    @toLeft.setter
    def toLeft(self, toLeft):
        self.__toleft = toLeft

class Mario(Object):

    def __init__(self, x, y):
        super().__init__(x,y)
        self.__states = {"toRight": True, "toLeft": False, "toBack": False}
        self.__height = 12
        self.__isUp = False
        self.__setJump = False

    def move_right(self):
        self.__states["toRight"] = True
        self.__states["toLeft"] = False
        self.__states["toBack"] = False
        self.x = self.x + 1

    def move_left(self):
        self.__states["toRight"] = False
        self.__states["toLeft"] = True
        self.__states["toBack"] = False
        self.x = self.x - 1

    def move_up(self):
        self.__states["toRight"] = False
        self.__states["toLeft"] = False
        self.__states["toBack"] = True
        self.y = self.y - 1

    def move_down(self):
        self.__states["toRight"] = False
        self.__states["toLeft"] = False
        self.__states["toBack"] = True
        self.y = self.y + 1

    def fall(self):
        self.y = self.y + 1

    def jumpUp(self):
        self.__height -= 1
        if self.__height > 3:
            self.y = self.y - 1.5

        if self.__height <= 0:
            self.__isUp = True

    def jumpDown(self):
        self.__height += 1
        if self.__height > 4:
            self.y = self.y + 1.5

        if self.__height == 12:
            self.__isUp = False
            self.__setJump = False


    @property
    def states(self):
        return self.__states
    @property
    def height(self):
        return self.__height
    @property
    def isUp(self):
        return self.__isUp
    @property
    def setJump(self):
        return self.__setJump
    @setJump.setter
    def setJump(self, setJump):
        self.__setJump = setJump
