import pytality
import data
import clickable
import event
import overlay
import random
import logging

log = logging.getLogger(__name__)

effect_text = dict(
    magic=dict(message="POWERFUL MAGIC", fg=pytality.colors.YELLOW),
    phys=dict(message="EXTRA STRONG", fg=pytality.colors.LIGHTMAGENTA),
    loot=dict(message="GREAT LOOT", fg=pytality.colors.LIGHTGREEN),
    terror=dict(message="TERRIFYING", fg=pytality.colors.LIGHTRED),
    durable=dict(message="RESISTANCE", fg=pytality.colors.BROWN)
)

class MonsterCard(clickable.ClickableBox):
    def __init__(self, parent=None, **kwargs):
        self.portrait = data.load_buffer(self.art_file, width=14, crop=True)

        self.name = pytality.buffer.PlainText(self.name, y=11, center_to=14, fg=pytality.colors.WHITE)
        self.line1 = pytality.buffer.PlainText(y=12, center_to=14, **effect_text[self.tags[0]])
        self.line2 = pytality.buffer.PlainText(y=13, center_to=14, **effect_text[self.tags[1]])

        self.overlay = overlay.Overlay(width=16, height=16, x=-1, y=-1)
        self.parent = parent
        self.mode = "in"
        super(MonsterCard, self).__init__(
            width=16, height=16,
            boxtype=pytality.boxtypes.BoxSingle,
            border_fg=pytality.colors.DARKGREY,
            children=[self.portrait, self.name, self.line1, self.line2, self.overlay],
            **kwargs
        )
        self.overlay.start("fade_in")

    def mouse_down(self, mx, my):
        if self.overlay.animation:
            return

        if self.mode != "fading_out":
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

    def __init__(self, **kwargs):
        super(CardDisplay, self).__init__(
            draw_bottom=False, draw_left=False, draw_right=False, padding_x=0,
            **kwargs
        )
        self.next_card_in = 0
        self.cards = [None] * self.slots

        self.title = pytality.buffer.PlainText("[ Available Monsters ]", y=-1, fg=pytality.colors.WHITE)
        self.title.x = (self.inner_width / 2) - (self.title.width / 2)
        self.children.append(self.title)

    def tick(self):
        if self.next_card_in:
            # dont finish the timer if we're full
            if self.next_card_in > 2 or None in self.cards:
                self.next_card_in -= 1

        if self.next_card_in <= 0 and None in self.cards:
            slot = self.cards.index(None)
            card_cls = random.choice(all_types)
            log.debug("Creating new card in slot %r, class is %r", slot, card_cls)
            card = card_cls(parent=self, x=(1 + slot * 17), x_offset=self.x + self.padding_x, y_offset=self.y + self.padding_y)

            self.children.append(card)
            clickable.register(card)
            self.cards[slot] = card

            self.next_card_in = self.card_delay
        for card in self.cards:
            if card:
                card.tick()

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
