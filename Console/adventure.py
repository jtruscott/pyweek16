import pytality
import event
import hero
import main
import overlay
import data
import random
import clickable
import time

import logging

log = logging.getLogger(__name__)

class World(object):
    # state goes here
    # fuck it, no instances, final destination, all class properties
    act = 1
    decisions = []

class Option(object):
    def __init__(self, text="", text_kwargs=None, choices=None, choice_kwargs=None, timeout=None):
        self.text = text
        self.text_kwargs = text_kwargs or {}
        self.choices = choices or []
        self.choice_kwargs = choice_kwargs or {}
        self.timeout = timeout

class Choice(clickable.ClickableBox):
    def __init__(self, adventure=None, text="", height=5, set=None, value=None, next=None, **kwargs):
        self.adventure = adventure
        self.inner_text = pytality.buffer.RichText(text, x=1, y=1)
        self.set = set
        self.value = value
        self.next = next
        super(Choice, self).__init__(
            height=height,
            width=self.inner_text.width + 4,
            children=[self.inner_text],
            boxtype=pytality.boxtypes.BoxSingle,
            border_fg=pytality.colors.DARKGREY,
            **kwargs
        )

    def mouse_down(self, mx, my):
        if not self.adventure.choice_clicked(self):
            return

options = dict(
    burn_1=Option(
        text="""
                                         <LIGHTRED>Burn Down The Village!</>


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer a sem aliquam purus congue fringilla ut ut magna.
Nulla accumsan porta ligula, eu lacinia arcu euismod et. Maecenas suscipit semper sem, sit amet facilisis erat blandit tincidunt.
Praesent scelerisque urna a ligula elementum dignissim. Vestibulum consequat tellus et nisl imperdiet semper.
Vestibulum mauris dui, commodo vitae consequat dapibus, varius non velit. Sed eget eros in lectus accumsan malesuada a quis turpis.
Vivamus quis est velit. Nam at cursus nibh.

Aenean tempus, eros eu dictum bibendum, dolor nulla laoreet <LIGHTGREEN>nibh</>, sollicitudin condimentum nunc purus vel turpis.
Curabitur a velit justo. Morbi euismod, turpis varius mollis luctus, diam augue tincidunt massa, ac auctor nibh justo vitae urna.
Fusce mollis pellentesque molestie. Donec non orci felis, ut ornare velit. Phasellus ut urna ac ligula gravida scelerisque.
Nunc posuere facilisis neque, vehicula congue odio venenatis sed. Donec scelerisque bibendum libero, id accumsan dui imperdiet quis.
Mauris quis lacus ante, et aliquet mauris. <WHITE>Aenean vel risus tortor</>. Nulla eleifend gravida turpis, sit amet malesuada massa
facilisis et. In hac habitasse platea dictumst. Maecenas tempus, turpis vel egestas ullamcorper, urna mi venenatis quam,
vel pharetra augue mi vitae odio. Quisque elementum blandit velit a iaculis. Donec lectus libero, viverra in vulputate id,
rutrum accumsan sapien. Vestibulum egestas molestie tempor.
""",
        text_kwargs=dict(y=5, x=10),
        choice_kwargs=dict(y=30, x=60),
        choices=[
            dict(set="killed_father", value=True, next="burn_2", text="Kill His Father!"),
            dict(set="killed_father", value=False, next="burn_2", text="Maim His Father!"),
        ]
    ),
    burn_2=Option(
        text="<YELLOW>Kill Everybody!",
        text_kwargs=dict(y=5, x=30),
        choice_kwargs=dict(y=10, x=40),
        choices=[
            dict(set="next_dungeon", value="crypt", next="end_act", text="Yes!"),
            dict(set="next_dungeon", value="orcs", next="end_act", text="No!"),
        ]
    ),
)

class Adventure(object):
    def __init__(self):
        clickable.unregister_all()

        self.root = pytality.buffer.Buffer(height=main.screen_height, width=main.screen_width)
        self.i = 0

    def load_option(self, key):
        option = options[key]
        self.choice_items = []

        self.root.children.append(pytality.buffer.RichText(option.text, **option.text_kwargs))
        for choice_settings in option.choices:
            kwargs = dict(choice_settings)
            kwargs.update(option.choice_kwargs)
            choice = Choice(adventure=self, **kwargs)

            if 'y' in option.choice_kwargs:
                option.choice_kwargs['y'] += choice.height + 1

            self.choice_items.append(choice)
            clickable.register(choice)
            self.root.children.append(choice)

        self.root.dirty = True

    def choice_clicked(self, choice):
        print choice, dir(choice)

    def tick(self):
        self.i += 1
        if self.i % 15 == 0:
            # safety margin
            self.root.dirty = True

    def draw(self):
        self.root.draw()

active_adventure = None

@event.on("adventure.setup")
def adventure_setup():
    global active_adventure
    active_adventure = Adventure()


@event.on("adventure.tick")
def adventure_tick():
    active_adventure.tick()


@event.on("adventure.draw")
def adventure_draw():
    active_adventure.draw()

import unittest


class Test(unittest.TestCase):
    def test_prompt(self):
        import game
        event.fire("hero.setup")
        event.fire("adventure.setup")
        active_adventure.load_option("burn_1")

        game.mode = "adventure"
        game.start()
