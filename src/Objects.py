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
        self.__states = {"normal": True, "toRight": False, "toLeft": False, "withBarrel": False, "inGrab": False}
        self.__movementTime = 30

    def grab(self):
        if self.__movementTime > 20:
            self.__states["normal"] = False
            self.__states["toLeft"] = True
            self.__movementTime -= 1
        elif self.__movementTime <= 20 and self.__movementTime > 10:
            self.__states["toLeft"] = False
            self.__states["withBarrel"] = True
            self.__movementTime -= 1
        elif self.__movementTime <= 10 and self.__movementTime > 0:
            self.__states["withBarrel"] = False
            self.__states["toRight"] = True
            self.__movementTime -= 1
        else:
            self.__states["toRight"] = False
            self.__states["normal"] = True
            self.__states["inGrab"] = False
            self.__movementTime = 30

    @property
    def states(self):
        return self.__states
    @property
    def movementTime(self):
        return self.__movementTime
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
        self.__states = {"upLeft": True, "upRight": False, "downRight": False, "downLeft": False, "toRight": True, "toLeft": False}

    def move_right(self):
        self.x = self.x + 0.25
        self.__states["toRight"] = True
        self.__states["toLeft"] = False

    def move_left(self):
        self.x = self.x - 0.25
        self.__states["toRight"] = False
        self.__states["toLeft"] = True

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

class Mario(Object):

    def __init__(self, x, y):
        super().__init__(x,y)
        self.__states = {"toRight": True, "toLeft": False, "toBack": False, "isUp": False, "inJump": False}
        self.__jumpHeight = 12

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
        self.__jumpHeight -= 1
        if self.__jumpHeight > 3:
            self.y = self.y - 1.5

        if self.__jumpHeight <= 0:
            self.states["isUp"] = True

    def jumpDown(self):
        self.__jumpHeight += 1
        if self.__jumpHeight > 4:
            self.y = self.y + 1.5

        if self.__jumpHeight == 12:
            self.states["isUp"] = False
            self.states["inJump"] = False


    @property
    def states(self):
        return self.__states
    @property
    def jumpHeight(self):
        return self.__jumpHeight
    @states.setter
    def states(self, states):
        self.__states = states
