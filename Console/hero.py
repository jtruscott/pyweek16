import pytality
import event
import data

class MoraleMeter(pytality.buffer.Buffer):
    def __init__(self, **kwargs):
        super(MoraleMeter, self).__init__(width=19, height=16, **kwargs)
        self.base = data.load_buffer('meter.ans', width=6, crop=True)
        self.meter = data.load_buffer('meter.ans', width=6, crop=True)
        self.text_lines = [
            pytality.buffer.RichText("<%s>- DESPONDENT", x=5, y=13),
            pytality.buffer.RichText("<%s>- APATHETIC", x=5, y=10),
            pytality.buffer.RichText("<%s>- DRIVEN", x=5, y=7),
            pytality.buffer.RichText("<%s>- HEROIC", x=5, y=4),
            pytality.buffer.RichText("<%s>- HOT BLOODED", x=5, y=1),
        ]
        self.children = [self.meter] + self.text_lines
        self.last_value = None

    def tick(self):
        if (active_hero.morale, active_hero.max_morale) == self.last_value:
            return

        self.last_value = (active_hero.morale, active_hero.max_morale)

        filled_rows = int(15.0 * active_hero.morale / active_hero.max_morale)
        for i, line in enumerate(self.text_lines):
            row_target = i*3 + 1
            if filled_rows >= row_target and filled_rows < row_target + 3:
                line.format(("WHITE",))
            else:
                line.format(("DARKGREY",))

        for row in range(15):
            y = 14 - row
            for x in (1, 2, 3):
                fg, bg, ch = self.base._data[y][x]
                if row > filled_rows:
                    self.meter._data[y][x] = [fg, bg, ch]
                else:
                    if row == 0 or row == 14:
                        if x == 1 or x == 3:
                            self.meter._data[y][x] = [fg, bg, ch]
                        elif row == 14:
                            self.meter._data[y][x] = [fg, pytality.colors.LIGHTRED, ch]
                        else:
                            self.meter._data[y][x] = [fg, pytality.colors.BLUE, ch]
                    else:
                        self.meter._data[y][x] = [fg, bg, '\xDB']
        self.meter.dirty = True

class StatDisplay(pytality.buffer.Box):
    def __init__(self, **kwargs):
        super(StatDisplay, self).__init__(**kwargs)
        self.title = pytality.buffer.PlainText("[ Hero Stats ]", y=-1, fg=pytality.colors.WHITE)
        self.title.x = (self.inner_width / 2) - (self.title.width / 2)
        self.hero_name = pytality.buffer.PlainText("BARTLEBUS THE MIGHTY", y=2, fg=pytality.colors.WHITE, center_to=self.inner_width)
        self.hero_level = pytality.buffer.PlainText("Level %i", y=3, fg=pytality.colors.LIGHTGREY, center_to=self.inner_width)
        self.hero_hp_text = pytality.buffer.RichText("", y=5)
        self.hero_hp_bar = pytality.buffer.Buffer(width=20, height=1, y=6, x=(self.inner_width / 2 - 10))

        self.monster_name = pytality.buffer.PlainText("", y=10, fg=pytality.colors.LIGHTGREY, center_to=self.inner_width)
        self.monster_hp_text = pytality.buffer.RichText("", y=11)

        self.battle_header = pytality.buffer.PlainText("BOSS BATTLE", y=10, fg=pytality.colors.LIGHTRED, center_to=self.inner_width, is_invisible=True)

        self.morale_meter = MoraleMeter(x=2, y=20)

        self.children.extend([
            self.title,
            self.hero_name,
            self.hero_level,
            self.hero_hp_text,
            self.hero_hp_bar,
            self.monster_name,
            self.monster_hp_text,
            self.battle_header,
            self.morale_meter
        ])

        self.mode = "dungeon"
        self.tick()

    def set_mode(self, mode):
        self.mode = mode
        if mode == "battle":
            self.monster_name.is_invisible = True
            self.monster_hp_text.is_invisible = True
            self.battle_header.is_invisible = False
        self.dirty = True

    def tick(self, owner=None):
        self.hero_level.format(active_hero.level)
        green_boxes = int(20.0 * active_hero.hp / active_hero.max_hp)

        hp_color = "WHITE"
        if green_boxes <= 10:
            hp_color = "YELLOW"
        if green_boxes <= 5:
            hp_color = "LIGHTRED"

        self.hero_hp_text.set(("HP <%s>%i</> / <WHITE>%i</>" % (hp_color, active_hero.hp, active_hero.max_hp)))
        self.hero_hp_text.x = (self.inner_width / 2) - (self.hero_hp_text.width / 2)

        for i in range(0, self.hero_hp_bar.width):
            if i < green_boxes:
                self.hero_hp_bar.set_at(x=i, y=0, fg=pytality.colors.LIGHTGREEN, bg=pytality.colors.GREEN, char='\xDF')
            else:
                self.hero_hp_bar.set_at(x=i, y=0, fg=pytality.colors.LIGHTRED, bg=pytality.colors.RED, char='\xDF')

        if self.mode == "dungeon":
            dungeon = owner
            if dungeon and dungeon.level.active_monster:
                monster = dungeon.level.active_monster
                self.monster_name.set(monster.name)
                self.monster_hp_text.set(("HP <WHITE>%i</> / <WHITE>%i</>" % (monster.hp, monster.max_hp)))
                self.monster_hp_text.x = (self.inner_width / 2) - (self.monster_hp_text.width / 2)
            else:
                self.monster_name.set("")
                self.monster_hp_text.set(" " * self.inner_width)
                self.monster_hp_text.x = 0
        else:
            battle = owner

        self.morale_meter.tick()

        import random
        active_hero.morale = random.randint(0, active_hero.max_morale)



class Hero(object):
    defeated = False
    in_combat = False

    regen_delay = 5
    regen_amount = 1

    def __init__(self):
        self.hp = 75
        self.max_hp = 100
        self.morale = 80
        self.max_morale = 100
        self.level = 1
        self.next_regen = 0
        self.attack = 10
        self.defense = 10
        self.m_defense = 10

    def lose_morale(self, loss):
        self.morale -= loss
        if self.morale <= 0:
            self.morale = 0
            self.defeated = True

    def gain_hp(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def end_combat(self, monster, dungeon):
        self.in_combat = False
        self.next_regen = self.regen_delay

    def dungeon_tick(self, dungeon):
        if not self.in_combat and self.hp < self.max_hp:
            if self.next_regen:
                self.next_regen -= 1
            if self.next_regen <= 0:
                self.next_regen = self.regen_delay
                self.gain_hp(self.regen_amount)

active_hero = None

@event.on("dungeon.setup")
def hero_setup():
    global active_hero
    active_hero = Hero()

