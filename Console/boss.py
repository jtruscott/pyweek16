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

exchanges = [
    dict(
        hero="""
Oh Father, I swear, by the fiery blood that courses in
both of our veins, I will strike down this demonic coward
who has spilled your sanguine life-force onto this dead earth!""",
        choices=[
            dict(title="SWING AND SNIPE", text="""
It does make the ground a rather nice shade of maroon.
I've got rugs that go well with all kinds of bloodstains.
Would you care to BROWSE MY CATALOGUE OF DEATH?"""),
            dict(title="VILLAINOUS GLOAT", text="""
Yes, yes! Your tears <WHITE>feed</> me, cowardly mortal! I can feel
the hatred saturating your heart! Let it consume you!
Become your hate, tiny human, and strike me down!
But not too hard, I just had this infernal, soul-forged plate buffed and polished.
Do you have any idea how many orphan souls it takes to get this sheen?"""),
        ]
    ),
    dict(
        hero="""
For all of the death you have caused, for all the misery you have sewn... for my
father, for my love, for all the people of this earth, my blade will destroy you! """,
        choices=[
            dict(title="SWING AND SNIPE", text="""
Your weak blows bounce off of my hardened skin! That can't be good for your blade.
All that vibration is gonna break it, and then you will be nothing before my
might! Also not much of an OW. That thing is sharp! What did you do, sharpen it
on the corpses of the damned? Also, die."""),
            dict(title="VILLAINOUS GLOAT", text="""
That's... not very likely. You'd do better if you block, like so. Then, you can
time your back stroke by how loud the tormented souls trapped in your - oh, wait,
no, you don't have that. Awkward. Well, here, you parry like - Oh, geeze. Um.
Yeah, go ahead, pick it back up, that's fine. Alright, where were we? """),
        ]
    ),
    dict(
        hero="""
Die, monster! Your hellish kind should have been exterminated centuries ago,
and your foul taint only stains the world with your vile filth!
My powerful blade will swing true and destroy all that you are, unspeakable fiend!""",
        choices=[
            dict(title="SWING AND SNIPE", text="""
Well, to be fair, I'm not actually a 'fiend', per se. More of a demon. The
difference is probably lost on you, but I can't imagine a little bleeding will be!
Or... something, I don't know. Here, just let me stab you."""),
            dict(title="VILLAINOUS GLOAT", text="""
My kin will rule this earth, and your skeleton shall crumble to ash beneath our feet
after a really, really long time. We'll be using your remains to pave the roads, of
course, and we'll need to enchant them pretty well so we don't crush them. Maybe you
and your dad will get to be road signs? But then we won't get to walk on your bones.
It's hard, being me..."""),
        ]
    ),
    dict(
        hero="""
he heart of this world cries out for your death, the tears of a thousand innocents
stain your skin, and by my strength and the vengeance that thrums in my soul,
I will vanquish you!""",
        choices=[
            dict(title="SWING AND SNIPE", text="""
A thousand innocents? Aw nuts, did it really dry up that quickly? I keep telling
Kernshebofell that the Tormented Flames of Oshtovenur just don't work for my
complexion! You've got to maintain your image, you know; do you think all of the
Mind Crushing Toil would really work out if us Overlords of the Year didn't look
like we bathed in the blood of virgins every morning! Here, let me give you a
better look... """),
            dict(title="VILLAINOUS GLOAT", text="""
The heart of the world is kind of a huge, molten rock. I've been down there.
It's warm. It doesn't really 'cry out' much, unless you count the sound of the
tortured dead we keep shoving into it. Maybe that's where all those volcanoes
are coming from. We might have to look into that. Thanks for that! We can always
use more people willing to put out new ideas and really get their head in the game."""),
        ]
    ),
]


class BattleSprite(pytality.buffer.Buffer):
    def __init__(self, width=16, height=16, crop=True, file_names=None, anim_delay=5, **kwargs):
        super(BattleSprite, self).__init__(width=width, height=width, **kwargs)
        self.sprites = [data.load_buffer(file_name, width=width, crop=crop) for file_name in file_names]
        self.overlay = overlay.Overlay(width=width, height=width, x=0, y=0)
        self.children = [self.sprites[0], self.overlay]
        self.anim_delay = self.anim_timer = anim_delay
        self.anim_index = 0

    def tick(self):
        self.overlay.tick(self)
        self.anim_timer -= 1
        if self.anim_timer <= 0:
            self.anim_timer = self.anim_delay
            self.anim_index += 1
            if self.anim_index >= len(self.sprites):
                self.anim_index = 0
            self.children = [self.sprites[self.anim_index], self.overlay]
            self.dirty = True

    def animate(self, anim_type, **kwargs):
        self.overlay.start(anim_type, owner=self.sprites[0], **kwargs)


class ClickableText(pytality.buffer.RichText):
    def __init__(self, on_mouse_down=None, **kwargs):
        self.on_mouse_down = on_mouse_down
        super(ClickableText, self).__init__(**kwargs)

    def mouse_in(self, x, y):
        self.dirty = True

    def mouse_out(self, x, y):
        self.dirty = True

    def mouse_down(self, x, y):
        #print 'down', self, x, y
        if self.on_mouse_down:
            self.on_mouse_down(self, x, y)


class ActionWindow(pytality.buffer.Box):
    def __init__(self, battle=None, **kwargs):
        super(ActionWindow, self).__init__(
            draw_bottom=False, draw_left=False, draw_right=False, padding_x=0,
            **kwargs
        )
        self.battle = battle

        self.title = pytality.buffer.PlainText("[ Battle Actions ]", y=-1, fg=pytality.colors.WHITE)
        self.title.x = (self.inner_width / 2) - (self.title.width / 2)
        self.children.append(self.title)


class Battle(object):
    def __init__(self, dungeon):
        sidebar_width = 26
        bottom_height = 17

        self.message_log = dungeon.message_log
        self.stat_display = dungeon.stat_display
        self.stat_display.set_mode("battle")
        clickable.unregister_all()


        self.battle_window = pytality.buffer.Buffer(
            x=sidebar_width,
            y=0,
            height=main.screen_height - bottom_height,
            width=main.screen_width - (sidebar_width * 2)

        )
        self.action_window = ActionWindow(
            width=main.screen_width - sidebar_width * 2,
            height=bottom_height,
            x=sidebar_width,
            y=main.screen_height - bottom_height,
            border_fg=pytality.colors.LIGHTGREY,
            battle=self,
        )
        self.action_overlay = overlay.Overlay(
            width=self.action_window.width,
            height=self.action_window.height - 1,
            x=0, y=0
        )

        self.real_boss = False
        if self.real_boss:
            self.boss_sprite = BattleSprite(file_names=["finalboss.ans"], width=61, height=48, x=self.battle_window.width - 61, y=0, crop=True)
            self.boss_portrait = data.load_buffer("finalbossport.ans", width=16, crop=True)
            sound.play_music("The_Final_Threat.mp3")
        else:
            self.boss_sprite = BattleSprite(file_names=["you2.ans", "you2alt.ans"], width=34, height=31, x=self.battle_window.width - 40, y=14, crop=True)
            self.boss_portrait = data.load_buffer("youport.ans", width=16, crop=True)
            sound.play_music("OHC_Changeling_Rumble.mp3")

        self.hero_sprite = BattleSprite(file_names=[hero.active_hero.get_boss_file()], width=18, height=15, x=10, y=30)
        self.hero_portrait = data.load_buffer("heroportrait.ans", width=16, crop=True)

        self.battle_window.children = [self.boss_sprite, self.hero_sprite]

        self.fullscreen_flash = pytality.buffer.Buffer(
            x=sidebar_width,
            height=main.screen_height,
            width=main.screen_width - (sidebar_width * 2)
        )

        self.root = pytality.buffer.Buffer(height=0, width=0, children=[
            self.message_log,
            self.stat_display,
            self.battle_window,
            self.action_window
        ])
        self.i = 0
        self.flashed = False
        self.message_log.add("\n     <LIGHTRED>BOSS BATTLE!")

        self.next_state = "hero_talk"
        self.after_animation_state = None
        self.state_delay = 5

    def tick(self):
        self.i += 1
        if self.i % 15 == 0:
            # safety margin
            self.root.dirty = True

        self.stat_display.tick(self)

        # animation tickers
        self.hero_sprite.tick()
        self.boss_sprite.tick()
        self.action_overlay.tick(self.action_overlay)

        if self.state_delay:
            self.state_delay -= 1

        if self.after_animation_state and not self.action_overlay.animation:
            self.next_state = self.after_animation_state
            self.after_animation_state = None
            self.state_delay = 0

        if self.state_delay is not None and self.state_delay <= 0:
            self.state_delay = None

            if self.next_state == "hero_talk":
                choice = random.choice(exchanges)
                self.show_dialog("hero", choice['hero'], "hero_attack", 0)
                self.next_choice = choice

            elif self.next_state == "hero_attack":
                self.hero_sprite.animate("flash")
                self.next_state = "hero_attack_2"
                self.state_delay = 6

            elif self.next_state == "hero_attack_2":
                self.boss_sprite.animate("flash", color=pytality.colors.LIGHTRED)
                self.next_state = "boss_choose"
                self.state_delay = 15

            elif self.next_state == "boss_choose":
                self.offer_choices(self.next_choice['choices'])

            elif self.next_state == "boss_attack":
                self.boss_sprite.animate("flash")
                self.next_state = "boss_attack_2"
                self.state_delay = 6

            elif self.next_state == "boss_attack_2":
                self.hero_sprite.animate("flash", color=pytality.colors.LIGHTRED)
                self.next_state = "hero_talk"
                self.state_delay = 15


    def show_dialog(self, source, text, next_state, state_delay=None):
        if source == "hero":
            portrait = self.hero_portrait
            title = "Altrune The Bold"
        else:
            portrait = self.boss_portrait
            if self.real_boss:
                title = "GRGRGFGR"
            else:
                title = "Skulltaker"

        portrait.x = 0
        portrait.y = 1
        title_buffer = pytality.buffer.PlainText(
            title.center(portrait.width),
            fg=pytality.colors.WHITE
        )
        title_buffer.x = 0
        title_buffer.y = 13

        text_buffer = ClickableText(
            message=text,
            x=19,
            x_offset=self.action_window.x,
            y_offset=self.action_window.y + 1,
            on_mouse_down=self.dismiss_dialog
        )
        text_buffer.y = (self.action_window.inner_height - text_buffer.height - 2) / 2
        text_buffer.children = [pytality.buffer.PlainText(
            "[ Click To Continue ]",
            center_to=text_buffer.width,
            y=text_buffer.height + 2,
            fg=pytality.colors.WHITE,
        )]
        text_buffer.next_state = next_state
        text_buffer.state_delay = state_delay
        clickable.register(text_buffer)

        self.action_window.children = [portrait, title_buffer, text_buffer]
        self.action_window.dirty = True

    def dismiss_dialog(self, dialog, x, y):
        clickable.unregister_all()
        self.action_window.children = [self.action_window.title, self.action_overlay]
        self.action_overlay.start("fade_out", anim_speed=256)

        self.next_state = None
        self.after_animation_state = dialog.next_state
        self.state_delay = dialog.state_delay

    def offer_choices(self, choices):
        self.choice_boxes = []
        self.action_window.children = [
            self.action_window.title,
            pytality.buffer.PlainText(
                message="Respond With:",
                center_to=self.action_window.width,
                y=1,
                fg=pytality.colors.WHITE,
            )
        ]

        for i, choice in enumerate(choices):
            text = pytality.buffer.RichText(choice['title'], y=1, x=1)
            choice_box = clickable.ClickableBox(
                width=40, height=8,
                x=8 + 47 * i, y=3,
                x_offset=self.action_window.x,
                y_offset=self.action_window.y + 1,
                boxtype=pytality.boxtypes.BoxSingle,
                border_fg=pytality.colors.DARKGREY,
                children=[text],
                on_mouse_down=self.box_clicked
            )
            choice_box.choice = choice
            self.choice_boxes.append(choice_box)
            clickable.register(choice_box)
            self.action_window.children.append(choice_box)

        self.action_window.dirty = True

    def box_clicked(self, box, x, y):
        clickable.unregister_all()

        self.show_dialog("you", box.choice['text'], "boss_attack", 0)

    def draw(self):
        self.root.draw()

        if not self.flashed:
            # ridiculous flashing animation
            # hopefully not too epileptic.
            for i in range(10):
                start = time.time()
                for row in self.fullscreen_flash._data:
                    for col in row:
                        if i in (0, 1, 7):
                            col[0] = pytality.colors.WHITE
                        elif i in (2, 6):
                            col[0] = pytality.colors.LIGHTGREY
                        elif i in (3, 5):
                            col[0] = pytality.colors.DARKGREY
                        else:
                            col[0] = pytality.colors.BLACK
                        col[2] = '\xDB'
                self.fullscreen_flash.draw(dirty=True)
                pytality.term.flip()
                # about 30fps.
                time.sleep(min(0.03, max(0, time.time() - start + 0.03)))
            self.flashed = True

            # we wiped these out just now
            self.battle_window.draw(dirty=True)
            self.action_window.draw(dirty=True)


active_battle = None


@event.on("boss.setup")
def boss_setup(dungeon):
    global active_battle
    active_battle = Battle(dungeon)


@event.on("boss.tick")
def boss_tick():
    active_battle.tick()


@event.on("boss.draw")
def boss_draw():
    active_battle.draw()


import unittest


class Test(unittest.TestCase):
    def test_generate(self):
        import dungeon
        import game
        event.fire("setup")
        event.fire("dungeon.setup")
        game.mode = "boss"
        event.fire("boss.setup", dungeon.active_dungeon)
        game.start()
