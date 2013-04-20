import pytality
import data
import clickable
import event
import overlay
import random
import logging
import collections

log = logging.getLogger(__name__)

effect_text = dict(
    magic=dict(message="POWERFUL MAGIC", fg=pytality.colors.YELLOW),
    phys=dict(message="EXTRA STRONG", fg=pytality.colors.LIGHTMAGENTA),
    loot=dict(message="GREAT LOOT", fg=pytality.colors.LIGHTGREEN),
    terror=dict(message="TERRIFYING", fg=pytality.colors.LIGHTRED),
    durable=dict(message="RESISTANCE", fg=pytality.colors.BROWN)
)

def combat(attack, defense, powerful=False, durable=False):
    attack_coeff = 10
    defense_coeff = 1
    powerful_coeff = 5
    durable_coeff = 1

    if powerful:
        attack_coeff += powerful_coeff

    if durable:
        defense_coeff += durable_coeff

    log.debug("starting values: attack %r defense %r attack coeff %r def coeff %r" % (attack, defense, attack_coeff, defense_coeff))

    attack = attack * attack_coeff
    defense = defense * defense_coeff

    log.debug("final attack: %r; defense: %r" % (attack, defense))

    return int(attack / defense)


class Monster(object):

    defeated = False
    stage = -1
    started = False

    powerful = False
    m_powerful = False
    durable = False

    hp = max_hp = 40
    attack = 10
    defense = 10

    xp_value = 15

    attack_type = 0 #0 for mixed magic/phys, 1 for phys only, 2 for magic only

    #log.debug("creating monster with attack type %r" % attack_type)

    def battle_tick(self, hero, hero_sprite, monster_sprite, dungeon):
        message_log = dungeon.message_log

        if not self.started:
            self.started = True
            message_log.add("")
            message_log.add("<WHITE>%s</> appears!" % self.name)
            hero.in_combat = True

            if 'durable' in self.tags:
                self.durable = True
                self.xp_value += 5
            if 'phys' in self.tags:
                self.powerful = True
                self.xp_value += 5
            if 'magic' in self.tags:
                self.m_powerful = True
                self.xp_value += 5
            if self.powerful and not self.m_powerful:
                self.attack_type = 1
            elif not self.powerful and self.m_powerful:
                self.attack_type = 2
            self.attack_current = self.attack_type



            if 'terror' in self.tags:
                self.xp_value += 5
                hero.lose_morale(10)
            else:
                hero.lose_morale(5)




        #print self.hp, self.stage
        if self.stage == 0:
            hero_sprite.set_at(0, 0, fg=pytality.colors.DARKGREY)
            message_log.add("The monster attacks!")

            if self.attack_type == 0:
                self.attack_current = random.randint(1, 2)

            log.debug("this tick, attack type %r" %self.attack_current)

            if self.attack_current == 1:
                log.debug("Phys attack, attack %r, def %r, powerful %r" % (self.attack,hero.defense,self.powerful))
                damage = combat(self.attack, hero.defense * hero.morale_multiplier(), self.powerful)
            elif self.attack_current == 2:
                log.debug("Mag attack, attack %r, def %r, powerful %r" % (self.attack,hero.m_defense,self.powerful))
                damage = combat(self.attack, hero.m_defense * hero.morale_multiplier(), self.m_powerful)
            else:
                message_log.add("ERROR: illegal attack type")

            hero.hp -= damage
            if hero.hp <= 0:
                hero.hp = hero.max_hp
                message_log.add("<LIGHTRED>Hero was defeated!")
                hero.defeated = True

        elif self.stage == 1:
            hero_sprite.set_at(0, 0, fg=pytality.colors.WHITE)

        elif self.stage < 6:
            pass

        elif self.stage == 6:
            monster_sprite.set_at(0, 0, fg=pytality.colors.RED)
            message_log.add("The hero strikes!")
            damage = combat(hero.attack * hero.morale_multiplier(), self.defense, False, self.durable)
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                monster_sprite.set_at(0, 0, fg=pytality.colors.LIGHTRED)
                message_log.add("<WHITE>%s</> is defeated!" % self.name)
                hero.end_combat(self, dungeon)
                self.defeated = True

        elif self.stage == 7:
            monster_sprite.set_at(0, 0, fg=pytality.colors.LIGHTRED)

        elif self.stage < 9:
            pass

        else:
            self.stage = -1
        self.stage += 1

class MonsterCard(clickable.ClickableBox, Monster):
    def __init__(self, parent=None, **kwargs):
        self.portrait = data.load_buffer(self.art_file, width=14, crop=True)

        self.name_text = pytality.buffer.PlainText(self.name, y=11, center_to=14, fg=pytality.colors.WHITE)
        self.line1 = pytality.buffer.PlainText(y=12, center_to=14, **effect_text[self.tags[0]])
        self.line2 = pytality.buffer.PlainText(y=13, center_to=14, **effect_text[self.tags[1]])

        self.overlay = overlay.Overlay(width=16, height=16, x=-1, y=-1)
        self.parent = parent
        self.mode = "in"
        super(MonsterCard, self).__init__(
            width=16, height=16,
            boxtype=pytality.boxtypes.BoxSingle,
            border_fg=pytality.colors.DARKGREY,
            children=[self.portrait, self.name_text, self.line1, self.line2, self.overlay],
            **kwargs
        )
        self.overlay.start("fade_in")

    def mouse_down(self, mx, my):
        if self.overlay.animation:
            return

        if self.mode != "fading_out":
            if self.parent and not self.parent.card_clicked(self):
                return
            self.overlay.start("fade_out")
            self.mode = "fading_out"
        else:
            self.overlay.start("fade_in")
            self.mode = "in"

    def tick(self):
        self.overlay.tick(self)
        if self.parent and self.mode == "fading_out" and not self.overlay.animation:
            self.parent.after_fade_out(self)

class Efreet(MonsterCard):
    name = "EFREET"
    tags = ["magic", "loot"]
    art_file = "efreet3.ans"

class KillerEye(MonsterCard):
    name = "KILLER EYE"
    tags = ["magic", "durable"]
    art_file = "killer eyed.ans"

class Dragon(MonsterCard):
    name = "DRAGON"
    tags = ["phys", "terror"]
    art_file = "dragon2.ans"

class Lich(MonsterCard):
    name = "LICH"
    tags = ["magic", "terror"]
    art_file = "lichd.ans"

class ArmorSpirit(MonsterCard):
    name = "ARMOR SPIRIT"
    tags = ["phys", "loot"]
    art_file = "living armor3d.ans"

class Mimic(MonsterCard):
    name = "MIMIC"
    tags = ["loot", "terror"]
    art_file = "mimicd.ans"

class Ogre(MonsterCard):
    name = "OGRE"
    tags = ["phys", "durable"]
    art_file = "ogred.ans"

class Pinata(MonsterCard):
    name = "PINATA"
    tags = ["loot", "durable"]
    art_file = "pinatagolem.ans"

class Shoggoth(MonsterCard):
    name = "SHOGGOTH"
    tags = ["durable", "terror"]
    art_file = "saggoth.ans"




all_types = MonsterCard.__subclasses__()

class CardDisplay(pytality.buffer.Box):
    card_delay = 5
    slots = 6

    def __init__(self, dungeon=None, monster_type=None, **kwargs):
        super(CardDisplay, self).__init__(
            draw_bottom=False, draw_left=False, draw_right=False, padding_x=0,
            **kwargs
        )
        self.dungeon = dungeon
        self.next_card_in = 0
        self.cards = [None] * self.slots
        self.monster_type = monster_type

        self.title = pytality.buffer.PlainText("[ Available Monsters ]", y=-1, fg=pytality.colors.WHITE)
        self.title.x = (self.inner_width / 2) - (self.title.width / 2)
        self.children.append(self.title)

    def pick_card(self):
        if self.monster_type == "fire":
            choices = all_types + [Dragon, Efreet] * 3
        elif self.monster_type == "crypt":
            choices = all_types + [Lich, ArmorSpirit] * 3
        elif self.monster_type == "ogre":
            choices = all_types + [Ogre, Mimic] * 3
        else:
            choices = all_types[:]

        # this isn't elegant, but clogged hands aren't very fun.
        for card_type, card_type_count in collections.Counter(type(x) for x in self.cards if x).items():
            if card_type_count >= 3:
                while card_type in choices:
                    choices.remove(card_type)

        return random.choice(choices)

    def tick(self):
        if self.next_card_in and not self.dungeon.level.active_monster:
            # and don't interact with the timer in combat
            # dont quite finish the timer if we're full
            if self.next_card_in > 5 or None in self.cards:
                self.next_card_in -= 1

        if self.next_card_in <= 0 and None in self.cards:
            slot = self.cards.index(None)
            card_cls = self.pick_card()
            log.debug("Creating new card in slot %r, class is %r", slot, card_cls)
            card = card_cls(parent=self, x=(1 + slot * 17), x_offset=self.x + self.padding_x, y_offset=self.y + self.padding_y)

            self.children.append(card)
            clickable.register(card)
            self.cards[slot] = card

            self.next_card_in = self.card_delay
        for card in self.cards:
            if card:
                card.tick()

    def card_clicked(self, card):
        if self.dungeon.level.active_monster:
            return False

        if not self.dungeon.level.move_path:
            return False

        self.dungeon.level.start_battle_with(card)
        return True

    def after_fade_out(self, card):
        clickable.unregister(card)
        self.children.remove(card)

        # collapse left
        self.cards.remove(card)

        for slot, card in enumerate(self.cards):
            if card:
                card.x = (1 + slot * 17)

        self.cards.append(None)
        self.dirty = True

import unittest
class Test(unittest.TestCase):
    def test_boxes(self):
        import game
        game.mode = 'test'
        root = pytality.buffer.Buffer(width=0, height=0)
        for i, cls in enumerate(all_types):
            p = cls(x=1 + i*17, y=20)
            clickable.register(p)
            root.children.append(p)

        @event.on('test.tick')
        def on_tick():
            for child in root.children:
                child.tick()

        @event.on('test.draw')
        def on_draw():
            root.draw()

        game.start()
