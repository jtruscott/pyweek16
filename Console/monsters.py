import pytality
import data
import clickable
import event
import overlay


effect_text = dict(
    magic=dict(message="POWERFUL MAGIC", fg=pytality.colors.YELLOW),
    phys=dict(message="EXTRA STRONG", fg=pytality.colors.LIGHTMAGENTA),
    loot=dict(message="GREAT LOOT", fg=pytality.colors.LIGHTGREEN),
    terror=dict(message="TERRIFYING", fg=pytality.colors.LIGHTRED),
    durable=dict(message="RESISTANCE", fg=pytality.colors.BROWN)
)

class MonsterCard(clickable.ClickableBox):
    def __init__(self, **kwargs):
        self.portrait = data.load_buffer(self.art_file, width=14, crop=True)

        self.name = pytality.buffer.PlainText(self.name, y=11, center_to=14, fg=pytality.colors.WHITE)
        self.line1 = pytality.buffer.PlainText(y=12, center_to=14, **effect_text[self.tags[0]])
        self.line2 = pytality.buffer.PlainText(y=13, center_to=14, **effect_text[self.tags[1]])

        self.overlay = overlay.Overlay(width=16, height=16, x=-1, y=-1)
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
        if self.mode != "out":
            self.overlay.start("fade_out")
            self.mode = "out"
        else:
            self.overlay.start("fade_in")
            self.mode = "in"

    def tick(self):
        self.overlay.tick(self)

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
