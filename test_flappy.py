from unittest import TestCase

from flappy import Bird, Tube


class TestBird(TestCase):
    def setUp(self):
        self.bird = Bird(x=0.2, y=0.5, width=0.1, height=0.1, y_acceleration=-0.001, y_flap=0.01)

    def test__step(self):
        x = self.bird.x
        y = self.bird.y

        self.bird.step()

        self.assertEqual(self.bird.x, x)
        self.assertLess(self.bird.y, y)

    def test__flap(self):
        x = self.bird.x
        y = self.bird.y

        self.bird.flap()
        self.bird.step()

        self.assertEqual(self.bird.x, x)
        self.assertGreater(self.bird.y, y)


class TestTube(TestCase):
    def setUp(self):
        self.bird = Bird(x=0.2, y=0.5, width=0.1, height=0.1, y_acceleration=-0.001, y_flap=0.01)

    def test__is_bird_knocked__left(self):
        tube = Tube(x=0.5, width=0.2, gate_y=0.01, gate_width=0.3, x_speed=-0.01)
        self.assertFalse(tube.is_bird_knocked(self.bird))

    def test__is_bird_knocked__begin__alive(self):
        tube = Tube(x=0.25, width=0.2, gate_y=0.4, gate_width=0.3, x_speed=-0.01)
        self.assertFalse(tube.is_bird_knocked(self.bird))

    def test__is_bird_knocked__begin__dead(self):
        tube = Tube(x=0.25, width=0.2, gate_y=0.2, gate_width=0.25, x_speed=-0.01)
        self.assertTrue(tube.is_bird_knocked(self.bird))

    def test__is_bird_knocked__inside__alive(self):
        tube = Tube(x=0.15, width=0.2, gate_y=0.4, gate_width=0.3, x_speed=-0.01)
        self.assertFalse(tube.is_bird_knocked(self.bird))

    def test__is_bird_knocked__inside__dead(self):
        tube = Tube(x=0.15, width=0.2, gate_y=0.55, gate_width=0.3, x_speed=-0.01)
        self.assertTrue(tube.is_bird_knocked(self.bird))

    def test__is_bird_knocked__end__alive(self):
        tube = Tube(x=0.05, width=0.2, gate_y=0.4, gate_width=0.3, x_speed=-0.01)
        self.assertFalse(tube.is_bird_knocked(self.bird))

    def test__is_bird_knocked__end__dead(self):
        tube = Tube(x=0.05, width=0.2, gate_y=0.2, gate_width=0.25, x_speed=-0.01)
        self.assertTrue(tube.is_bird_knocked(self.bird))

    def test__is_bird_knocked__right(self):
        tube = Tube(x=0.0, width=0.1, gate_y=0.01, gate_width=0.3, x_speed=-0.01)
        self.assertFalse(tube.is_bird_knocked(self.bird))

    def test__step(self):
        tube = Tube(x=0.5, width=0.2, gate_y=0.01, gate_width=0.3, x_speed=-0.01)
        tube.step()
        self.assertLess(tube.x, 0.5)