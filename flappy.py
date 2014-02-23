import random


class GameOver(Exception):
    def __init__(self, score, reason=''):
        self.score = score
        self.reason = reason

    def __str__(self):
        return "GameOver, score: %i %s" % (self.score, self.reason)


class Game(object):
    def __init__(self, settings):
        self.bird = Bird(settings.BIRD_X, settings.BIRD_Y,
                         settings.BIRD_SIZE, settings.BIRD_SIZE,
                         settings.BIRD_Y_SPEED_ACCELERATION, settings.BIRD_Y_SPEED_FLAP)

        self.tube_factory = TubeFactory(settings.TUBE_WIDTH, settings.GATE_WIDTH,
                                        settings.TUBE_SPEED, settings.INITIAL_TUBE_X)

        self.world = World(self.bird, self.tube_factory, settings.SPACE_BETWEEN_TUBES)

    @property
    def score(self):
        return self.world.passed_tubes_number

    def step(self):
        self.world.step()

    def reset(self):
        self.bird.reset()
        self.world.reset()


class World(object):
    def __init__(self, bird, tube_factory, space_between_tubes):
        assert space_between_tubes > 0

        self.__bird = bird
        self.__tube_factory = tube_factory

        self.__tubes = []
        self.__current_tube = None
        self.__tubes_distance = tube_factory.tube_width + space_between_tubes
        self.__passed_tubes_number = 0

    @property
    def tubes(self):
        return self.__tubes

    @property
    def passed_tubes_number(self):
        return self.__passed_tubes_number

    def step(self):
        self.__bird.step()

        for tube in self.__tubes:
            tube.step()

        self.__delete_and_add_tubes()
        self.__check_is_bird_alive()

    def reset(self):
        self.__passed_tubes_number = 0
        self.__tubes = []

    def __delete_and_add_tubes(self):
        if self.__tubes:
            # remove tubes at the left
            if self.__tubes[0].x + self.__tubes[0].width < 0:
                del self.__tubes[0]

            # add tubes to the right
            last_tube_shift = 1 - self.__tubes[-1].x
            if last_tube_shift >= self.__tubes_distance:
                self.__create_tube()

            # check if current tube passed
            if self.__current_tube.x_right < self.__bird.x:
                current_tube_number = self.__tubes.index(self.__current_tube) + 1
                self.__current_tube = self.__tubes[current_tube_number]
                self.__passed_tubes_number += 1
        else:
            self.__create_tube()
            self.__current_tube = self.__tubes[0]

        assert self.__tubes and self.__current_tube
        assert self.__current_tube in self.__tubes

    def __check_is_bird_alive(self):
        if self.__is_bird_knocked_by_ground():
            raise GameOver(self.__passed_tubes_number, reason="knocked by ground")

        if self.__current_tube and self.__current_tube.is_bird_knocked(self.__bird):
            raise GameOver(self.__passed_tubes_number, reason="knocked by tube")

    def __is_bird_knocked_by_ground(self):
        return self.__bird.y <= 0 or self.__bird.y + self.__bird.height >= 1

    def __create_tube(self):
        self.__tubes.append(self.__tube_factory.create())


class Bird(object):
    def __init__(self, x, y, width, height, y_acceleration, y_flap):
        assert 0 < width < 1 and 0 < height < 1
        assert x > 0 and y > 0
        assert x + width < 1 and y + height < 1
        assert y_acceleration < 0 < y_flap

        self.__x = x
        self.__initial_y = y
        self.__y = self.__initial_y
        self.__width = width
        self.__height = height
        self.__y_acceleration = y_acceleration
        self.__y_flap = y_flap

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

    def step(self):
        self.__y_speed += self.__y_acceleration
        self.__y += self.__y_speed

    def flap(self):
        if self.__y_speed < 0:
            self.__y_speed = 0
        self.__y_speed += self.__y_flap

    def reset(self):
        self.__y = self.__initial_y
        self.__y_speed = 0


class Tube(object):
    def __init__(self, x, width, gate_y, gate_width, x_speed):
        assert gate_y > 0 and gate_y + gate_width < 1

        self.__x = x
        self.__width = width
        self.__gate_y = gate_y
        self.__gate_width = gate_width
        self.__x_speed = x_speed

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
        self.__x += self.__x_speed

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
    def __init__(self, tube_width, gate_width, tube_speed, initial_tube_x):
        self.__tube_width = tube_width
        self.__gate_width = gate_width
        self.__tube_speed = tube_speed
        self.__initial_tube_x = initial_tube_x

    @property
    def tube_width(self):
        return self.__tube_width

    def create(self):
        gate_y = random.random() * (1 - self.__gate_width)
        return Tube(self.__initial_tube_x, self.__tube_width, gate_y, self.__gate_width, self.__tube_speed)

