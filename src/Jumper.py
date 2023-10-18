import kivy

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.label import Label


class MainScreen(Screen):
    pass


class InstructionScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.canPress = True

    def resetPress(self, dt):
        self.canPress = True


class GameScren(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.canPress = True
        self.counter = 0
        self.score = 0
        self.obstacle_speed = 5.0

    def resetPress(self, dt):
        self.canPress = True

    def jump_anim(self):
        anim = Animation(y=self.ids.beany.ids.meany.pos[1] + 175, duration=0.6, t='out_quad')
        anim += Animation(y=self.ids.beany.ids.meany.pos[1], duration=0.6, t='in_quad')
        anim.start(self.ids.beany.ids.meany)
        self.canPress = False

    def move_left_anim(self):
        anim1 = Animation(x=self.ids.sorky.pos[0] - 1000, duration=5.)

        anim1.start(self.ids.sorky)

    def changeFork(self):
        self.ids.sorky.source = 'assets/images/newFork.png'

    def checkCollision(self, dt):
        if self.ids.sorky.pos[0] <= self.ids.beany.ids.meany.pos[0] + 90 <= self.ids.sorky.pos[0] + self.ids.sorky.size[
            0] / 2:
            if self.ids.sorky.pos[1] <= self.ids.beany.ids.meany.pos[1] - 25 <= self.ids.sorky.pos[1] + \
                    self.ids.sorky.size[1] / 2:
                self.manager.current = 'ded'

    def secondCounter(self, dt):
        self.counter += 1
        self.ids.txt = "%s Seconds" % self.counter

    def calltimer(self):
        Clock.schedule_interval(self.secondCounter, 1)

    def collisionSchedule(self):
        Clock.schedule_interval(self.checkCollision, .02)

    def checkanimdone(self):
        Clock.schedule_interval(self.resetFork, 5)

    def resetFork(self, dt):
        self.ids.sorky.pos = (Window.width, Window.height - 710)
        self.move_left_anim()
        self.score += 1


class Bean(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self.canPress = True

    def resetPress(self, dt):
        self.canPress = True

    def jump_anim(self):
        anim = Animation(x=self.ids.beany.pos[0], y=self.ids.beany.pos[1] + 100, duration=.55, t='out_circ')

        anim += Animation(x=self.ids.beany.pos[0], y=self.ids.beany.pos[1], duration=.55, t='out_circ')

        anim.start(self.ids.beany)


class Die_Screen(Screen):
    pass


class Fork(Widget):
    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)

    def move_left_anim(self):
        anim1 = Animation(x=self.ids.forky.pos[0] - 1000, duration=4.5)
        anim1.start(self.ids.forky)


class Counter(Label):
    score = 0

    def __init__(self, **kwargs):
        super(Counter, self).__init__(**kwargs)
        Clock.schedule_interval(self._increment_a, 1.)

    def _increment_a(self, dt):
        self.score += 1


Builder.load_file('src/Jumper.kv')

class TestApp(App):
    def __init__(self):
        App.__init__(self)
        self.sm = ScreenManager()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.sm.add_widget(MainScreen(name='main'))
        self.gam = GameScren(name='game')
        self.sm.add_widget(self.gam)
        self.inst = InstructionScreen(name="instr")
        self.sm.add_widget(self.inst)
        self.counter = 1
        self.dead = Die_Screen(name='ded')
        self.sm.add_widget(self.dead)
        self.title = "Bean Jump"

    def build(self):
        return self.sm

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar' or keycode[1] == 'w' or keycode[1] == 'up':
            if self.sm.current == 'game':
                if self.gam.canPress:
                    self.gam.jump_anim()
                    Clock.schedule_once(self.gam.resetPress, 1.6)
            elif self.sm.current == 'instr':
                if self.inst.canPress:
                    self.inst.jump_anim()
                    Clock.schedule_once(self.inst.resetPress, 1.5)

    def start_fork(self):
        if self.sm.current == 'game':
            self.gam.move_left_anim()

    def switch_to_game(self, inst):
        self.sm.current = 'game'

    def switch_to_game2(self, inst):
        self.sm.current = 'game'

    def switch_to_game3(self, inst):
        self.sm.current = 'ded'

    def quick_game(self, inst):
        quit()

    def imager(self, inst):
        self.counter += 1
        if self.counter % 2 == 0:
            inst.background_normal = 'assets/images/audiooff.png'
        else:
            inst.background_normal = 'assets/images/audioon.png'


if __name__ == '__main__':
    TestApp().run()
