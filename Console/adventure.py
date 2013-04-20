import pytality
import event
import hero
import main
import overlay
import data
import random
import clickable
import time
import sound

import logging

log = logging.getLogger(__name__)

class World(object):
    # state goes here
    # fuck it, no instances, final destination, all class properties
    act = 1
    decisions = []
    next_dungeon = None
    finding = None

class Option(object):
    def __init__(self, text="", text_kwargs=None, choices=None, choice_kwargs=None, timeout=None):
        self.text = text
        self.text_kwargs = text_kwargs or {}
        self.choices = choices or []
        self.choice_kwargs = choice_kwargs or {}
        self.timeout = timeout

class Choice(clickable.ClickableBox):
    def __init__(self, adventure=None, text="", height=5, set=None, value=None, next=None, morale_bonus=0, **kwargs):
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
        self.morale_bonus = morale_bonus

        children = [self.inner_text]
        if 'children' in kwargs:
            children.extend(kwargs['children'])
            del kwargs['children']

        super(Choice, self).__init__(
            height=height,
            width=self.inner_text.width + 4,
            children=children,
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
\n\n\n\n\n\n\n\n\n\n\n\n
                    You are Skulltaker, a sinister villain if there ever was one.

                    You want to take over the world and rule it with an iron evil fist,
                    but there's just one problem. According to the legends, an ancient
                    cosmic evil will soon awaken and destroy the world that you intend to
                    rule.

                    That won't do at all. But the legends also tell of a great and powerful
                    hero, who will rise from humble beginnings to save the world from
                    destruction at the hands of evil. And you know just who the prophecy
                    says is going to be that hero.


\n\n\n\n\n\n\n\n\n\n\n\n
                    This is Altrune. And he doesn't have what it takes to save the world.

                    So you're going to train him to greatness, so he can save it for you.
                    And after that all that's over, well, you can deal with him then.
""",
        text_kwargs=dict(y=7, x=15, initial_color=pytality.colors.BLACK, bg=pytality.colors.WHITE, children=[
            data.load_buffer("youport-white.ans", width=18, max_height=12, crop=True, x=45, y=0),
            data.load_buffer("heroportrait-white.ans", width=18, max_height=12, crop=True, x=45, y=26)
        ]),
        choice_kwargs=dict(
            y=53
        ),
        choices=[
            dict(next="burn_2", text="   OK   ", x=63, y=53),
        ]
    ),
    burn_2=Option(
        text="""
                    Let's start by giving Altrune something to be heroic about.

                    Hero types always get <RED>SO MAD</> when you burn down their villages.
                    And his hometown of Idylburg is looking very flammable today.

                    So we'll take a torch to his little hometown... And look here!
                    Altrune's father is home! And so is the love of Altrune's life!



                    You could kidnap his girlfriend and run away to the Fire Temple.
                    I bet Altrune wouldn't like that at all, and would hunt you down for it.
                    Heroes love rescuing a damsel in distress, after all.



                    Or you could kill his father and steal the priceless family shield.
                    You could let him know that you're keeping the shield in the Ogre
                    Stronghold. Altrune would probably want that shield so bad he'd trudge
                    through an entire den of angry ogres, just to get it back.



                    Or maybe you'd rather just kill everyone that he knows and loves,
                    and then raise them as zombies in your Evil Crypt Lair.
                    I'm sure that'd make Altrune pretty angry.



                    You don't have enough time to do more than one of those, though.

                    Decisions, decisions.

""",
        text_kwargs=dict(x=10, y=12, initial_color=pytality.colors.BLACK, bg=pytality.colors.WHITE),
        choice_kwargs=dict(y=51, height=7),
        choices=[
            dict(set="next_dungeon", value="fire", next="end_act1", text="Kidnap his girlfriend\n        at the\n      Fire Temple!", x=25, morale_bonus=70),
            dict(set="next_dungeon", value="ogre", next="end_act1", text="  Steal the shield   \n    and store it\n   with the Ogres!", x=55, morale_bonus=50),
            dict(set="next_dungeon", value="crypt", next="end_act1", text="    Kill everyone\n and raise zombies \n    in the Crypt!", x=85, morale_bonus=60),
        ]
    ),
    fetch_1=Option(
        text="""
                    That went pretty well. It looks like Altrune is a fast learner!



                    But his equipment is still pretty shabby. You're trying to set
                    him up to stop an ancient, world-devouring cosmic force, and a
                    puny sword and some armor that probably came from the thrift
                    store isn't really going to cut it.



                    You know of a couple artifacts that should be pretty powerful in
                    the hands of a hero backed by that much prophecy. You can't just
                    walk up and GIVE them to Altrune, of course, that wouldn't be very
                    sporting. But he's a straightforward fellow, just drop a couple
                    hints and he'll go charging off to find the mystical equipment.



                    You could send him to the Eldritch Dragons in the Fire-Lorne Peaks,
                    where they keep the legendary <BROWN>Sword Of The Ages</>. If Altrune got that
                    sword, it would give him a respectable boost in offensive might.
                    It would probably look snazzy too, crackling with arcane power.



                    Or maybe you should start Altrune off with the <BROWN>Armor Of the Ages</>,
                    which is being kept in the Haunted Tomb under the Pellentian Ocean.
                    That armor would give him a significant increase in his defensive
                    staying power. More importantly, you've heard it looks pretty cool.



                    What piece of equipment will you lead Altrune into acquiring?

""",
        text_kwargs=dict(x=10, y=12, initial_color=pytality.colors.BLACK, bg=pytality.colors.WHITE),
        choice_kwargs=dict(y=51, height=6),
        choices=[
            dict(set="next_dungeon", value="fire", next="end_act2", text=" Get the Sword Of The Ages \nfrom the Eldritch Dragons", x=30, morale_bonus=80),
            dict(set="next_dungeon", value="crypt", next="end_act2", text=" Get the Armor Of The Ages \n  from the Haunted Tomb", x=70, morale_bonus=80),
        ]
    ),
    final_1=Option(
        text="""
                    Excellent! Now we just have to lead Altrune to the other artifact,
                    and he'll be decked out and ready for when the ancient evil awakens.


\n\n\n\n\n\n\n\n\n\n\n\n

                                  <MAGENTA>GRLARLBLRLLBLLLABLRLALBLABLBLAALBLABLLBLAL</>



                    Oh. Oh dear.


                    That wasn't supposed to happen yet.


                    Well, it looks like there's no time for artifacts. The World-Devourer
                    is waking up early, and the only person that can stop it is Altrune.


                    And Altrune doesn't exactly know about the World-Devourer yet.


                    Well, I suppose you ought to lead Altrune right at you, right now,
                    so those two powerhouses can get to know each other better.


                    Let's hope this works!

""",
        text_kwargs=dict(x=10, y=9, initial_color=pytality.colors.BLACK, bg=pytality.colors.WHITE, children=[
            data.load_buffer("finalbossport-white.ans", width=18, max_height=12, crop=True, x=45, y=5),
        ]),
        choice_kwargs=dict(y=53, height=5),
        choices=[
            dict(set="next_dungeon", value=None, next="end_act3", text="   OK   ", x=63, y=53, morale_bonus=50),
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

    def start_act(self):
        clickable.unregister_all()
        sound.play_music("Relax.mp3")
        if World.act == 1:
            self.load_option("burn_1")

        elif World.act == 2:
            self.load_option("fetch_1")

        else:
            self.load_option("final_1")

        World.act += 1

    def choice_clicked(self, choice):
        clickable.unregister_all()

        if choice.set:
            setattr(World, choice.set, choice.value)

        if choice.morale_bonus:
            hero.active_hero.morale += choice.morale_bonus
            if hero.active_hero.morale > 100:
                hero.active_hero.morale = 100

        if choice.next == "end_act1":
            if World.next_dungeon == "ogre":
                World.finding = "shield"

        if choice.next == "end_act2":
            if World.next_dungeon == "fire":
                World.finding = "sword"
            else:
                World.finding = "armor"


        if "end_act" in choice.next:
            import game
            event.fire("dungeon.setup", World.next_dungeon)
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
        active_adventure.load_option("final_1")

        game.mode = "adventure"
        game.start()
