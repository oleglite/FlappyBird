# coding=utf-8

import random


class GameOver(Exception):
    def __init__(self, score, reason=''):
        self.score = score
        self.reason = reason

    def __str__(self):
        return "GameOver, score: %i %s" % (self.score, self.reason)


class Game(object):
    BIRD_SIZE = 0.05
    BIRD_X = 0.2
    BIRD_Y = 0.6

    def __init__(self):
        self.bird = Bird(self.BIRD_X, self.BIRD_Y, self.BIRD_SIZE, self.BIRD_SIZE)
        self.tube_factory = TubeFactory(tube_width=0.1, gate_width=0.25)
        self.world = World(self.bird, self.tube_factory, 0.3)


    @property
    def score(self):
        return self.bird.passed_tubes_number

    def step(self):
        self.world.step()

    def restart(self):
        self.bird = Bird(self.BIRD_X, self.BIRD_Y, self.BIRD_SIZE, self.BIRD_SIZE)
        self.world.bird = self.bird
        self.world.restart()


class World(object):
    def __init__(self, bird, tube_factory, tubes_distance):
        assert tubes_distance > 0

        self.bird = bird
        self.__tube_factory = tube_factory

        self.__tubes = []
        self.__current_tube = None
        self.__tubes_distance = tube_factory.tube_width + tubes_distance

    @property
    def tubes(self):
        return self.__tubes

    def step(self):
        self.bird.step()

        for tube in self.__tubes:
            tube.step()

        self.__delete_and_add_tubes()
        self.__check_is_bird_alive()

    def restart(self):
        self.__tubes = []

    def __delete_and_add_tubes(self):
        if self.__tubes:
            # удаляем трубы слева
            if self.__tubes[0].x + self.__tubes[0].width < 0:
                del self.__tubes[0]

            # добавляем трубы справа
            last_tube_shift = 1 - self.__tubes[-1].x
            if last_tube_shift >= self.__tubes_distance:
                self.__create_tube()

            # проверяем пролетели ли мы текущую трубу
            if self.__current_tube.x_right < self.bird.x:
                current_tube_number = self.__tubes.index(self.__current_tube) + 1
                self.__current_tube = self.__tubes[current_tube_number]
                self.bird.tube_passed()
        else:
            self.__create_tube()
            self.__current_tube = self.__tubes[0]

        assert self.__tubes and self.__current_tube
        assert self.__current_tube in self.__tubes

    def __check_is_bird_alive(self):
        if self.__is_bird_knocked_by_ground():
            raise GameOver(self.bird.passed_tubes_number, reason="knocked by ground")

        if self.__current_tube and self.__current_tube.is_bird_knocked(self.bird):
            raise GameOver(self.bird.passed_tubes_number, reason="knocked by tube")

    def __is_bird_knocked_by_ground(self):
        return self.bird.y <= 0 or self.bird.y + self.bird.height >= 1

    def __create_tube(self):
        self.__tubes.append(self.__tube_factory.create())


class Bird(object):
    __Y_SPEED_INCREMENT = 0.0006
    __Y_SPEED_FLAP = 0.013

    def __init__(self, x, y, width, height):
        assert 0 < width < 1 and 0 < height < 1
        assert x > 0 and y > 0
        assert x + width < 1 and y + height < 1

        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

        self.__passed_tubes_number = 0
        self.__y_speed = 0

    @property
    def x(self):
        return self.__x

    @property
    def x_right(self):
        return self.__x + self.__width

    @property
    def y(self):
        return self.__y

    @property
    def y_bottom(self):
        return self.__y + self.__height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def passed_tubes_number(self):
        return self.__passed_tubes_number

    def step(self):
        self.__y_speed += self.__Y_SPEED_INCREMENT
        self.__y -= self.__y_speed

    def flap(self):
        if self.__y_speed > 0:
            self.__y_speed = 0
        self.__y_speed -= self.__Y_SPEED_FLAP

    def tube_passed(self):
        self.__passed_tubes_number += 1


class Tube(object):
    __TUBE_SPEED = 0.005

    def __init__(self, x, width, gate_y, gate_width):
        assert gate_y > 0 and gate_y + gate_width < 1

        self.__x = x
        self.__width = width
        self.__gate_y = gate_y
        self.__gate_width = gate_width

    @property
    def x(self):
        return self.__x

    @property
    def x_right(self):
        return self.__x + self.__width

    @property
    def width(self):
        return self.__width

    @property
    def gate_y(self):
        return self.__gate_y

    @property
    def gate_width(self):
        return self.__gate_width

    def step(self):
        self.__x -= self.__TUBE_SPEED

    def is_bird_knocked(self, bird):
        if bird.y > self.__gate_y and bird.y_bottom < self.__gate_y + self.__gate_width:
            return False

        if bird.x_right < self.x or bird.x > self.__x + self.__width:
            return False

        return True

    def __repr__(self):
        return "Tube(x=%s, width=%s, gate_y=%s, gate_width=%s)" % (
            self.__x, self.__width, self.__gate_y, self.__gate_width
        )


class TubeFactory(object):
    __INITIAL_TUBE_X = 1

    def __init__(self, tube_width, gate_width):
        self.__tube_width = tube_width
        self.__gate_width = gate_width

    @property
    def tube_width(self):
        return self.__tube_width

    def create(self):
        gate_y = random.random() * (1 - self.__gate_width)
        return Tube(self.__INITIAL_TUBE_X, self.__tube_width, gate_y, self.__gate_width)

