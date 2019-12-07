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

    @property
    def states(self):
        return self.__states
