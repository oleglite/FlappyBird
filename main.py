from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse

from flappy import Game, GameOver


class ScreenScale(object):
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size

    def to_pixels(self, game_x, game_y):
        """
        >>> scale = ScreenScale((800, 600))
        >>> scale.to_pixels(1, 1)
        (800, 600)
        >>> scale.to_pixels(0.1, 0.1)
        (80.0, 60.0)
        """
        return self.screen_width * game_x, self.screen_height * game_y


class GameWidget(Widget):
    BIRD_COLOR = (1, 0, 0)
    TUBE_COLOR = (0, 1, 0)

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)

        Window.bind(on_key_down=self.on_key_down)

        import settings
        self.game = Game(settings)
        self.__scale = ScreenScale(self.size)

        self.bind(pos=self.update_screen)
        self.bind(size=self.update_screen)

    def update_screen(self, *args):
        if args:
            self.__scale = ScreenScale(self.size)
        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Color(*self.BIRD_COLOR)
            Ellipse(
                pos=self.__scale.to_pixels(self.game.bird.x, self.game.bird.y),
                size=self.__scale.to_pixels(self.game.bird.width, self.game.bird.height)
            )

            Color(*self.TUBE_COLOR)
            for tube in self.game.world.tubes:
                Rectangle(
                    pos=self.__scale.to_pixels(tube.x, 0),
                    size=self.__scale.to_pixels(tube.width, tube.gate_y)
                )

                top_gate_y = tube.gate_y + tube.gate_width
                Rectangle(
                    pos=self.__scale.to_pixels(tube.x, top_gate_y),
                    size=self.__scale.to_pixels(tube.width, 1 - top_gate_y)
                )

            Label(font_size=70, center_x=self.width / 2, top=self.top - 30, text=str(self.game.score))

    def step(self, dt):
        try:
            self.game.step()
        except GameOver as e:
            self.game.reset()
        self.update_canvas()

    def on_touch_down(self, touch):
        self.game.bird.flap()

    def on_key_down(self, *args):
        self.game.bird.flap()


class FlappyBirdApp(App):
    def build(self):
        FPS = 60
        game = GameWidget()
        Clock.schedule_interval(game.step, 1. / FPS)
        return game



if __name__ == '__main__':
    FlappyBirdApp().run()