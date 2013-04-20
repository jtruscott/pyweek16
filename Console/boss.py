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
import monsters
import adventure

exchanges = [
#This row has exactly 82 characters in it This row has exactly 82 characters in it
    dict(
        hero="""
Oh Father, I swear, by the fiery blood that courses in both of our veins, I will
strike down this demonic coward who has spilled your sanguine life-force onto this
dead earth!""",
        choices=[
            dict(title="SWING AND SNIPE", text="""
It does make the ground a rather nice shade of maroon. I've got rugs that go well
with all kinds of bloodstains. Would you care to BROWSE MY CATALOGUE OF DEATH?"""),
            dict(title="VILLAINOUS GLOAT", text="""
Yes, yes! Your tears <WHITE>feed</> me, cowardly mortal! I can feel the hatred saturating
your heart! Let it consume you! Become your hate, tiny human, and strike me down!
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
and your foul taint only stains the world with your vile filth! My mighty blade
shall swing true and destroy all that you are, unspeakable fiend!""",
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
I will cut you down, creature of the night! The force of a thousand suns will
drive my blade into your degenerate flesh, disgusting fiend, and their rage will
burn away your evil from this earth!""",
        choices=[
            dict(title="SWING AND SNIPE", text="""
You know, I saw someone put the math together on that once. Some kind of
magnifying death ray. It's a lot harder than you think. You'd probably break your
arm like that. I prefer something more along the lines of 'the amount of pressure
required to drag a serrated blade through gross anatomy'. Here, like this!"""),
            dict(title="VILLAINOUS GLOAT", text="""
I could use a bit of a searing; it helps maintain my diabolical good looks. It's
no accident I've been Overlord of the Year, three years running. It takes a lot of
effort to murder that many children, to glower that hatefully, you know?"""),
        ]
    ),
    dict(
        hero="""
The heart of this world cries out for your death, the tears of a thousand innocents
stain your skin, and by my strength and the vengeance that thrums in my soul,
I will vanquish you!""",
        choices=[
            dict(title="SWING AND SNIPE", text="""
A thousand innocents? Aw nuts, did it really dry up that quickly? I keep telling
Kernshebofell that the Tormented Flames of Oshtovenur just don't work for my
complexion! You've got to maintain your image, you know; do you think all of the
Mind Crushing Toil would really work out if us Overlords of the Year didn't look
like we bathed in the blood of virgins every morning! Here, let me give you a
better look..."""),
            dict(title="VILLAINOUS GLOAT", text="""
The heart of the world is kind of a huge, molten rock. I've been down there.
It's warm. It doesn't really 'cry out' much, unless you count the sound of the
tortured dead we keep shoving into it. Maybe that's where all those volcanoes
are coming from. We might have to look into that. Thanks for that! We can always
use more people willing to put out new ideas and really get their head in the game."""),
        ]
    ),
    dict(
        hero="""
Your evil armies were as nothing before me, cur. I have destroyed your allies, and
I have burnt your stronghold to the ground! Now, I will finish this, by taking
your head and ending your evil reign!""",
        choices=[
            dict(title="SWING AND SNIPE", text="""
Oh no, my evil hordes! Whatever will I do? Oh, that's right. Use the secondary
evil hordes. Or the tertiary. Or the... let's just say I've got a lot of evil
hordes, okay? They don't exactly take a lot of training or management. Some of
them even literally grow on trees! That, or I can just kill you myself."""),
            dict(title="VILLAINOUS GLOAT", text='''
You know, it's not just a team effort. Every member of our group is ambitious,
we've all got a lot of strong ideas and a lot of good principals. You can't just
want the group to succeed, you have to want YOU to succeed, you know? Takes real
drive and personality, you need to be a real go-getter, the kind of guy who wakes
up in the morning and says "Self, I'm going to burn an entire city to the ground
today, and I'm going to do it for me."'''),
        ]
    ),
    dict(
        hero="""
You monster! Look at the evil you have wrought! The land is ash before you, and
the polluted waters run black under a weeping sun! For all the hell you have
brought to this earth, I will destroy you!""",
        choices=[
            dict(title="SWING AND SNIPE", text="""
Honestly, I'm just getting started. It's going to take months to really despoil
the world and break open the sky, releasing the shrieking hordes of eternal night.
That kind of thing takes planning, it takes resources, and it takes the right
attitude. If you can't say 'no' to slacking, you'll always say 'yes' to lacking."""),
            dict(title="VILLAINOUS GLOAT", text="""
I know! I was particularly proud of all the ash. I kept those hellfires stoked for
days! Our draconic hordes are really dedicated to achieving the most optimal
results. Fireblood the Soulburner was looking great for a promotion, too! I mean,
until you lopped off his head. That was depressing. Oh well, thousands more
blood-crazed, psychotic dragons where he came from, I guess!"""),
        ]
    ),

#This row has exactly 82 characters in it This row has exactly 82 characters in it
]


class BattleSprite(pytality.buffer.Buffer):
    def __init__(self, width=16, height=16, crop=True, file_names=None, anim_delay=5, **kwargs):
        super(BattleSprite, self).__init__(width=width, height=height, **kwargs)
        self.sprites = [data.load_buffer(file_name, width=width, crop=crop, max_height=height) for file_name in file_names]
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
    def __init__(self, dungeon, final_boss):
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

        self.real_boss = final_boss
        if self.real_boss:
            self.boss_sprite = BattleSprite(file_names=["finalboss.ans"], width=61, height=48, x=self.battle_window.width - 61, y=0, crop=True)
            self.boss_portrait = data.load_buffer("finalbossport.ans", width=16, crop=True)
            sound.play_music("The_Final_Threat.mp3")
        else:
            self.boss_sprite = BattleSprite(file_names=["you2.ans", "you2alt.ans"], width=34, height=31, x=self.battle_window.width - 40, y=14, crop=True)
            self.boss_portrait = data.load_buffer("youport.ans", width=16, crop=True)
            sound.play_music("OHC_Changeling_Rumble.mp3")

        act = (adventure.World.act - 1)
        self.boss_attack = 13 + (7 * act)
        self.boss_defense = 8 + (7 * act)
        self.boss_hp = self.boss_max_hp = 60 + (20 * act)

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

        self.pending_attack_type = None
        self.pending_attack_powerful = False

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
                if self.pending_attack_type:
                    if self.pending_attack_type == "phys":
                        self.message_log.add("The boss strikes!")
                        damage = monsters.combat(self.boss_attack, hero.active_hero.defense * hero.active_hero.morale_multiplier(), powerful=self.pending_attack_powerful, durable=False)
                        self.message_log.add("%s damage!" % damage)
                        hero.active_hero.hp -= damage
                    else:
                        self.message_log.add("The boss uses magic!")
                        damage= monsters.combat(self.boss_attack, hero.active_hero.m_defense * hero.active_hero.morale_multiplier(), powerful=self.pending_attack_powerful, durable=False)
                        self.message_log.add("%s damage!" % damage)
                        hero.active_hero.hp -= damage

                    self.pending_attack_type = None

                    if hero.active_hero.hp <= 0:
                        self.message_log.add("The hero is defeated!")
                        clickable.unregister_all()
                        hero.active_hero.hp = 0
                        self.hero_sprite.animate("fade_out", anim_speed=3, restrict=True)
                        self.next_state = "hero_defeated"
                        self.state_delay = len(self.hero_sprite.overlay.empty_cells) / 3 + 5

                    elif not self.real_boss:
                        hero.active_hero.morale += 5
                        if self.pending_attack_powerful:
                            hero.active_hero.morale += 10

                        if hero.active_hero.morale > 100:
                            hero.active_hero.morale = 100

                if hero.active_hero.hp > 0:
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
                self.message_log.add("The hero strikes!")
                damage = monsters.combat(hero.active_hero.attack * hero.active_hero.morale_multiplier(), self.boss_defense, powerful=False, durable=False)
                self.message_log.add("%s damage!" % damage)
                self.boss_hp -= damage
                if self.boss_hp <= 0:
                    self.message_log.add("The boss is defeated!")
                    clickable.unregister_all()
                    self.boss_hp = 0
                    self.boss_sprite.animate("fade_out", anim_speed=12, restrict=True)
                    self.next_state = "boss_defeated"
                    self.state_delay = len(self.boss_sprite.overlay.empty_cells) / 12 + 5
                else:
                    self.offer_choices(self.next_choice['choices'])

            elif self.next_state == "boss_attack":
                self.boss_sprite.animate("flash")
                self.next_state = "boss_attack_2"
                self.state_delay = 6

            elif self.next_state == "boss_attack_2":
                self.hero_sprite.animate("flash", color=pytality.colors.LIGHTRED)
                self.next_state = "hero_talk"
                self.state_delay = 15

            elif self.next_state == "boss_defeated":
                import game
                if self.real_boss:
                    game.mode = "victory"
                    event.fire("victory.setup")
                else:
                    game.mode = "adventure"
                    adventure.active_adventure.start_act()

            elif self.next_state == "hero_defeated":
                import game
                game.mode = "defeat"
                event.fire("defeat.setup")


    def show_dialog(self, source, text, next_state, state_delay=None):
        if source == "hero":
            portrait = self.hero_portrait
            title = "Altrune The Bold"
        else:
            portrait = self.boss_portrait
            if self.real_boss:
                title = "World-Devourer"
            else:
                title = "Skulltaker"

        portrait.x = 1
        portrait.y = 1
        title_buffer = pytality.buffer.PlainText(
            title.center(portrait.width),
            fg=pytality.colors.WHITE
        )
        title_buffer.x = 1
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

        self.action_window.children = [self.action_window.title, portrait, title_buffer, text_buffer]
        self.action_window.dirty = True

    def dismiss_dialog(self, dialog, x, y):
        clickable.unregister_all()
        self.action_window.children = [self.action_window.title, self.action_overlay]
        self.action_overlay.start("fade_out", anim_speed=256)

        self.next_state = None
        self.after_animation_state = dialog.next_state
        self.state_delay = dialog.state_delay

    def offer_choices(self, choices):

        if self.real_boss:
            self.pending_attack_type = random.choice(["phys", "magic"])
            self.pending_attack_powerful = random.choice([False, True])
            text = "<LIGHTMAGENTA>" + random.choice([
                "GRAAAALRGLARGLARLGALRLLALGLLLALLLGLLALGLLAGRLRLALBLBBALGBLBALGBLBLABLAGLALALFL",
                "GLOORPAAAARPLLALARALRALAPAPRLAPARLALAPRALLPARPAAAAARLPALAAALPALLPALPALPALAAAPL",
                "AAAGLGLGLAPRALGPALRAPLAGAAAAARGAGLAGPARALPAAAALPGLARAPLAGAAAALRLPARLPAALAAAALL",
            ] + [
                ''.join(random.choice('GLARB') for _ in range(80))
                for __ in range(5)
            ]
            )
            self.show_dialog("you", text, "boss_attack", 0)
            return

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
        box_width = 40
        power_attack = random.choice([0, 1])
        for i, choice in enumerate(choices):
            attack_type = random.choice(["phys", "magic"])
            attack_powerful = (i == power_attack)

            box_children = [
                pytality.buffer.RichText(choice['title'].center(box_width-2), y=1, x=0),
            ]
            if attack_type == "phys":
                box_children.append(pytality.buffer.PlainText("Physical Attack", fg=pytality.colors.LIGHTMAGENTA, center_to=box_width-2, y=3, x=0))
            else:
                box_children.append(pytality.buffer.PlainText("Magical Attack", fg=pytality.colors.YELLOW, center_to=box_width-2, y=3, x=0))

            if attack_powerful:
                box_children.append(pytality.buffer.PlainText("Powerful", fg=pytality.colors.RED, center_to=box_width-2, y=4, x=0))

            choice_box = clickable.ClickableBox(
                width=box_width, height=8,
                x=8 + 47 * i, y=3,
                x_offset=self.action_window.x,
                y_offset=self.action_window.y + 1,
                boxtype=pytality.boxtypes.BoxSingle,
                border_fg=pytality.colors.DARKGREY,
                children=box_children,
                on_mouse_down=self.box_clicked
            )
            choice_box.choice = choice

            choice_box.attack_type = attack_type
            choice_box.attack_powerful = attack_powerful

            self.choice_boxes.append(choice_box)
            clickable.register(choice_box)
            self.action_window.children.append(choice_box)

        self.action_window.dirty = True

    def box_clicked(self, box, x, y):
        clickable.unregister_all()

        self.pending_attack_type = box.attack_type
        self.pending_attack_powerful = box.attack_powerful

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
    hero.active_hero.hp = hero.active_hero.max_hp

    if adventure.World.finding == "shield":
        dungeon.message_log.add("Hero found: \n<WHITE>\x07</> <BROWN>Family Shield</>")
        hero.active_hero.has_shield = True
        hero.active_hero.gain_stat('defense', 10, dungeon.message_log)
        hero.active_hero.gain_stat('m_defense', 10, dungeon.message_log)

    if adventure.World.finding == "sword":
        dungeon.message_log.add("Hero found: \n<WHITE>\x07</> <BROWN>Sword Of The Ages</>")
        hero.active_hero.has_sword = True
        hero.active_hero.gain_stat('attack', 10, dungeon.message_log)

    if adventure.World.finding == "armor":
        dungeon.message_log.add("Hero found: \n<WHITE>\x07</> <BROWN>Armor Of The Ages</>")
        hero.active_hero.has_armor = True
        hero.active_hero.gain_stat('defense', 5, dungeon.message_log)
        hero.active_hero.gain_stat('m_defense', 5, dungeon.message_log)

    adventure.World.finding = None

    global active_battle
    active_battle = Battle(dungeon, final_boss=(adventure.World.act > 3))


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
        event.fire("adventure.setup")
        #adventure.active_adventure.start_act()
        #adventure.active_adventure.start_act()
        #adventure.active_adventure.start_act()
        event.fire("dungeon.setup")
        game.mode = "boss"
        event.fire("boss.setup", dungeon.active_dungeon)
        game.start()
