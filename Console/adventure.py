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
        self.inner_text = pytality.buffer.RichText(
            text,
            x=1, y=1,
            initial_color=pytality.colors.BLACK,
            bg=pytality.colors.LIGHTGREY
        )
        self.set = set
        self.value = value
        self.next = next
        super(Choice, self).__init__(
            height=height,
            width=self.inner_text.width + 4,
            children=[self.inner_text],
            boxtype=pytality.boxtypes.BoxSingle,
            border_bg=pytality.colors.BROWN, border_fg=pytality.colors.YELLOW,
            interior_bg=pytality.colors.LIGHTGREY, interior_fg=pytality.colors.BLACK,
            hover_interior_bg=pytality.colors.WHITE, hover_interior_fg=pytality.colors.BLACK,
            hover_border_bg=pytality.colors.BROWN, hover_border_fg=pytality.colors.WHITE,
            **kwargs
        )

    def mouse_in(self, mx, my):
        self.inner_text.bg = pytality.colors.WHITE
        self.inner_text.update_data()
        super(Choice, self).mouse_in(mx, my)

    def mouse_out(self, mx, my):
        self.inner_text.bg = pytality.colors.LIGHTGREY
        self.inner_text.update_data()
        super(Choice, self).mouse_out(mx, my)

    def mouse_down(self, mx, my):
        if not self.adventure.choice_clicked(self):
            return

options = dict(
    burn_1=Option(
        text="""
                               <RED>Burn Down The Village!</>


  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer a sem aliquam

Nulla accumsan porta ligula, eu lacinia arcu euismod et. Maecenas suscipit semper

  blandit tincidunt. Praesent scelerisque urna a ligula elementum dignissim.

  imperdiet semper. Vestibulum mauris dui, commodo vitae consequat dapibus,

accumsan malesuada a quis turpis. Vivamus quis est velit. Nam at cursus nibh.
""",
        text_kwargs=dict(y=25, x=25, initial_color=pytality.colors.BLACK, bg=pytality.colors.WHITE),
        choice_kwargs=dict(
            y=50,
        ),
        choices=[
            dict(set="killed_father", value=True, next="burn_2", text="Kill His Father!", x=35),
            dict(set="killed_father", value=False, next="burn_2", text="Maim His Father!", x=65),
        ]
    ),
    burn_2=Option(
        text="<YELLOW>Kill Everybody!",
        text_kwargs=dict(x=25, y=25),
        choice_kwargs=dict(y=50),
        choices=[
            dict(set="next_dungeon", value="crypt", next="end_act", text="Yes!", x=40),
            dict(set="next_dungeon", value="orcs", next="end_act", text="No!", x=60),
        ]
    ),
)

class Adventure(object):
    def __init__(self):
        clickable.unregister_all()
        hero.stat_display.set_mode("adventure")

        self.root = pytality.buffer.Buffer(height=main.screen_height, width=main.screen_width - main.sidebar_width)
        self.frame_l = data.load_buffer("frame-l.ans", width=80, crop=False)
        self.frame_r = data.load_buffer("frame-r.ans", width=49, crop=True)
        self.frame_r.x = 80
        self.i = 0

    def load_option(self, key):
        log.debug("loading option %r", key)
        option = options[key]
        self.root.children = [hero.stat_display, self.frame_l, self.frame_r]
        self.choice_items = []

        self.root.children.append(pytality.buffer.RichText(option.text, **option.text_kwargs))
        for choice_settings in option.choices:
            kwargs = dict(choice_settings)
            kwargs.update(option.choice_kwargs)
            choice = Choice(adventure=self, **kwargs)

            #if 'y' in option.choice_kwargs:
            #    option.choice_kwargs['y'] += choice.height + 1

            self.choice_items.append(choice)
            clickable.register(choice)
            self.root.children.append(choice)

        self.root.dirty = True

    def choice_clicked(self, choice):
        clickable.unregister_all()

        if choice.set:
            setattr(World, choice.set, choice.value)

        if choice.next == "end_act":
            import game
            event.fire("dungeon.setup")
            game.mode = "dungeon"
        else:
            self.load_option(choice.next)

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
        event.fire("setup")
        event.fire("adventure.setup")
        active_adventure.load_option("burn_1")

        game.mode = "adventure"
        game.start()
