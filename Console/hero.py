import pytality
import event
import data
import random

class MoraleMeter(pytality.buffer.Buffer):
    def __init__(self, **kwargs):
        super(MoraleMeter, self).__init__(width=19, height=16, **kwargs)
        self.base = data.load_buffer('meter.ans', width=6, crop=True)
        self.meter = data.load_buffer('meter.ans', width=6, crop=True)
        self.title = pytality.buffer.PlainText("HERO MORALE", y=-2, fg=pytality.colors.WHITE, center_to=self.width)
        self.text_lines = [
            pytality.buffer.RichText("<%s>- DESPONDENT\n  <%s>-10%% stats</>", x=5, y=13),
            pytality.buffer.RichText("<%s>- APATHETIC\n  <%s>-5%% stats</>", x=5, y=10),
            pytality.buffer.RichText("<%s>- DRIVEN\n  <%s></>", x=5, y=7),
            pytality.buffer.RichText("<%s>- HEROIC\n  <%s>+10%% stats</>", x=5, y=4),
            pytality.buffer.RichText("<%s>- HOT BLOODED\n  <%s>+20%% stats</>", x=5, y=1),
        ]
        self.children = [self.title, self.meter] + self.text_lines
        self.last_value = None

    def tick(self, mode):
        if (active_hero.morale, active_hero.max_morale, mode) == self.last_value:
            return

        self.last_value = (active_hero.morale, active_hero.max_morale, mode)

        filled_rows = int(15.0 * active_hero.morale / active_hero.max_morale)
        for i, line in enumerate(self.text_lines):
            row_target = i*3 + 1
            if filled_rows >= row_target and filled_rows < row_target + 3:
                if mode == "dungeon" or mode == "battle":
                    if filled_rows > 7:
                        line.format(("WHITE", "LIGHTGREEN"))
                    else:
                        line.format(("WHITE", "LIGHTRED"))
                else:
                    line.format(("WHITE", "BLACK"))
            else:
                line.format(("DARKGREY", "BLACK"))

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

        self.hero_name = pytality.buffer.PlainText("Altrune The Bold", y=2, fg=pytality.colors.WHITE, center_to=self.inner_width)
        self.hero_level = pytality.buffer.PlainText("Level %i", y=3, fg=pytality.colors.LIGHTGREY, center_to=self.inner_width)
        self.hero_hp_text = pytality.buffer.RichText("", y=5)
        self.hero_hp_bar = pytality.buffer.Buffer(width=21, height=1, y=6, x=(self.inner_width / 2 - 10))

        self.hero_xp_text = pytality.buffer.RichText("", y=8)
        self.hero_xp_bar = pytality.buffer.Buffer(width=21, height=1, y=9, x=(self.inner_width / 2 - 10))

        self.hero_stat_text = pytality.buffer.RichText("", y=11, x=0)
        self.hero_equipment_text = pytality.buffer.RichText("", y=15, x=0)

        self.monster_name = pytality.buffer.PlainText("", y=22, fg=pytality.colors.LIGHTGREY, center_to=self.inner_width)
        self.monster_hp_text = pytality.buffer.RichText("", y=23)
        self.monster_hp_bar = pytality.buffer.Buffer(width=21, height=1, y=24, x=(self.inner_width / 2 - 10))

        self.morale_meter = MoraleMeter(x=2, y=47)

        self.children.extend([
            self.title,
            self.hero_name,
            self.hero_level,
            self.hero_hp_text,
            self.hero_hp_bar,
            self.hero_xp_text,
            self.hero_xp_bar,
            self.hero_stat_text,
            self.hero_equipment_text,
            self.monster_name,
            self.monster_hp_text,
            self.monster_hp_bar,
            self.morale_meter
        ])

        self.mode = "adventure"
        self.tick()

    def set_mode(self, mode):
        self.mode = mode
        if mode == "battle":
            self.monster_name.is_invisible = False
            self.monster_hp_text.is_invisible = False
            self.monster_hp_bar.is_invisible = False
            self.hero_stat_text.is_invisible = False
        elif mode == "dungeon":
            self.monster_name.is_invisible = False
            self.monster_hp_text.is_invisible = False
            self.hero_stat_text.is_invisible = False
            self.monster_hp_bar.is_invisible = True
        else:
            self.monster_name.is_invisible = True
            self.monster_hp_text.is_invisible = True
            self.hero_stat_text.is_invisible = False
            self.monster_hp_bar.is_invisible = True
        self.dirty = True

    def tick(self, owner=None):
        self.hero_level.format(active_hero.level)

        # Hero HP
        green_boxes = int(float(self.hero_hp_bar.width) * active_hero.hp / active_hero.max_hp)

        hp_color = "WHITE"
        if green_boxes <= 10:
            hp_color = "YELLOW"
        if green_boxes <= 5:
            hp_color = "LIGHTRED"

        self.hero_hp_text.set(("  HP <%s>%i</> / <WHITE>%i</>  " % (hp_color, active_hero.hp, active_hero.max_hp)))
        self.hero_hp_text.x = (self.inner_width / 2) - (self.hero_hp_text.width / 2)

        for i in range(0, self.hero_hp_bar.width):
            if i < green_boxes:
                self.hero_hp_bar.set_at(x=i, y=0, fg=pytality.colors.LIGHTGREEN, bg=pytality.colors.GREEN, char='\xDF')
            else:
                self.hero_hp_bar.set_at(x=i, y=0, fg=pytality.colors.LIGHTRED, bg=pytality.colors.RED, char='\xDF')

        # Hero Stats
        self.hero_stat_text.set(
            (
                " <LIGHTGREY>  ATK: </><WHITE>%- 2i</>  <LIGHTGREY> DEF: </><WHITE>%- 3i</>  \n"
                "             <LIGHTGREY>MDEF: </><WHITE>%- 3i</>  \n"
            ) % (active_hero.attack, active_hero.defense, active_hero.m_defense)
        )

        # Hero XP
        yellow_boxes = int(float(self.hero_xp_bar.width) * active_hero.xp / active_hero.max_xp)

        self.hero_xp_text.set("  EXP <BROWN>%i</> / <YELLOW>%i</>  " % (active_hero.xp, active_hero.max_xp))
        self.hero_xp_text.x = (self.inner_width / 2) - (self.hero_xp_text.width / 2)

        for i in range(0, self.hero_xp_bar.width):
            if i < yellow_boxes:
                self.hero_xp_bar.set_at(x=i, y=0, fg=pytality.colors.YELLOW, bg=pytality.colors.BROWN, char='\xDF')
            else:
                self.hero_xp_bar.set_at(x=i, y=0, fg=pytality.colors.LIGHTGREY, bg=pytality.colors.DARKGREY, char='\xDF')

        # Hero Equipment
        equipment_lines = ["<BROWN>%s</>\n" % "Hero Equipment".center(self.inner_width)]
        if active_hero.has_sword:
            #equipment_lines.append(" <LIGHTGREY>Weapon:</>")
            equipment_lines.append(" <BROWN>\x07</> <YELLOW>Sword Of The Ages</>")
        if active_hero.has_shield:
            #equipment_lines.append(" <LIGHTGREY>Shield:</>")
            equipment_lines.append(" <BROWN>\x07 Family Shield</>")
        if active_hero.has_armor:
            #equipment_lines.append(" <LIGHTGREY>Armor:</>")
            equipment_lines.append(" <BROWN>\x07</> <YELLOW>Armor Of The Ages</>")

        for equipment_key in active_hero.equipment_slots:
            if equipment_key in active_hero.equipment:
                #equipment_lines.append(" <LIGHTGREY>%s:</>" % equipment_key)
                equipment_lines.append(" <BROWN>\x07 %s</>" % active_hero.equipment[equipment_key])
        self.hero_equipment_text.set("\n".join(equipment_lines))

        # Dungeon Stuff
        if self.mode == "dungeon":
            dungeon = owner
            if dungeon and dungeon.level.active_monster:
                monster = dungeon.level.active_monster
                start_y = max(20, self.hero_equipment_text.height + self.hero_equipment_text.y + 2)
                self.monster_name.set(monster.name)
                self.monster_name.y = start_y
                self.monster_hp_text.set((" HP <WHITE>%i</> / <WHITE>%i</> " % (monster.hp, monster.max_hp)))
                self.monster_hp_text.x = (self.inner_width / 2) - (self.monster_hp_text.width / 2)
                self.monster_hp_text.y = start_y + 1
            else:
                self.monster_name.set("")
                self.monster_hp_text.set(" " * self.inner_width)
                self.monster_hp_text.x = 0
        else:
            battle = owner
            if battle:
                start_y = max(25, self.hero_equipment_text.height + self.hero_equipment_text.y + 3)
                # Boss HP
                if battle.real_boss:
                    self.monster_name.set("World-Devourer")
                else:
                    self.monster_name.set("Skulltaker")

                self.monster_hp_text.set((" HP <WHITE>%i</> / <WHITE>%i</> " % (battle.boss_hp, battle.boss_max_hp)))
                self.monster_hp_text.x = (self.inner_width / 2) - (self.monster_hp_text.width / 2)

                self.monster_name.y = start_y
                self.monster_hp_text.y = start_y + 1
                self.monster_hp_bar.y = start_y + 2

                green_boxes = int(float(self.monster_hp_bar.width) * battle.boss_hp / battle.boss_max_hp)

                hp_color = "WHITE"
                if green_boxes <= 10:
                    hp_color = "YELLOW"
                if green_boxes <= 5:
                    hp_color = "LIGHTRED"

                for i in range(0, self.monster_hp_bar.width):
                    if i < green_boxes:
                        self.monster_hp_bar.set_at(x=i, y=0, fg=pytality.colors.LIGHTGREEN, bg=pytality.colors.GREEN, char='\xDF')
                    else:
                        self.monster_hp_bar.set_at(x=i, y=0, fg=pytality.colors.LIGHTRED, bg=pytality.colors.RED, char='\xDF')

        self.morale_meter.tick(self.mode)

active_hero = None
stat_display = None


class Hero(object):
    defeated = False
    in_combat = False

    regen_delay = 2
    regen_amount = 1

    def __init__(self):
        self.hp = self.max_hp = 100
        self.next_regen = 0

        self.morale = 27 # Every 20 after this puts you in a new bracket
                        # so if choice 1 gives 40 morale, that puts hero in bracket 3
        self.max_morale = 100

        self.xp = 0
        self.max_xp = 100

        self.level = 1
        self.attack = 10
        self.defense = 10
        self.m_defense = 10

        self.equipment_slots = [
            'Ring',
            'Amulet',
            'Periapt',
            'Torc',
            'Gorget',
            'Hauberk',
            'Faulds',
            'Gauntlets',
            'Bracers',
            'Armbands',
            'Pauldrons',
            'Besagues',
            'Vambraces',
            'Tassets',
            'Sabatons',
            'Greaves',
            'Chasuble',
            'Surcoat',
            'Cloak',
            'Cape',
            'Robes',
            'Gloves',
            'Headband',
            'Goggles'
        ]
        self.equipment = {}

        self.has_shield = False
        self.has_sword = False
        self.has_armor = False

    def get_boss_file(self):
        if self.has_shield:
            if self.has_sword:
                return "herodshs.ans"
            if self.has_armor:
                return "herodsha.ans"
            return "herodsh.ans"

        if self.has_sword:
            return "herods.ans"
        if self.has_armor:
            return "heroda.ans"

        return "hero3.ans"

    def morale_multiplier(self):
        #REMOVE THIS FOR FINAL - DEBUG TESTING ONLY
        #return 1

        # i checked and these are the exact brackets.
        # it's a little weird because of the line rounding.
        if self.morale > 86:
            return 1.2
        if self.morale > 66:
            return 1.1
        if self.morale > 46:
            return 1.0
        if self.morale > 26:
            return 0.95
        return 0.9

    def make_item(self, power, message_log):
        enchantments = [
            #123456789
            'Power',
            'Toughness',
            'Swiftness',
            'Puissance',
            'Repelling',
            'Quickness',
            'Dexterity',
            'Charisma',
            'Wisdom',
            'Elvenkind',
            'Archery',
            'Flight',
            'Shielding',
            'Valhalla',
            'Fireballs',
            'Eyes',
            'Accuracy',
            'Alacrity',
            'Fortune',
            'The Fox',
            'Haste',
            'Health',
            'The Ox',
            'The Tiger',
            'The Otter',
            'The Boar'
            #123456789
        ]
        slot = random.choice(self.equipment_slots)
        enchantment = random.choice(enchantments)
        name = "%s of %s" % (slot, enchantment)
        self.equipment[slot] = name
        effect = random.choice(['attack', 'defense', 'm_defense'])
        message_log.add("Hero found: \n<WHITE>\x07</> <BROWN>%s</>" % name)
        self.gain_stat(effect,power,message_log)

    def gain_stat(self,stat,gain,message_log):
        setattr(self, stat, getattr(self, stat) + gain)

        stat_text = {
            'attack' : 'Attack',
            'defense' : 'Defense',
            'm_defense' : 'M.Defense',
            'max_hp' : 'Max HP',
            'hp' : 'HP',
            'xp' : 'XP'
        }

        message_log.add("Hero gains +%i %s!" % (gain, stat_text[stat]))

    def lose_morale(self, loss):
        self.morale -= loss
        if self.morale <= 0:
            self.morale = 0
            self.defeated = True
            import game
            game.mode = "defeat"
            event.fire("moraledefeat.setup")

    def gain_hp(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def end_combat(self, monster, dungeon):
        self.in_combat = False
        self.next_regen = self.regen_delay
        self.xp += monster.xp_value
        dungeon.message_log.add("Gained %i XP!" % monster.xp_value)
        if self.xp >= self.max_xp:
            dungeon.message_log.add("")
            dungeon.message_log.add("<YELLOW>Hero leveled up!")
            self.level += 1
            self.xp -= self.max_xp
            self.gain_stat('max_hp',10,dungeon.message_log) #ew ew gross. but it's a fix.
            self.hp = self.max_hp
            self.gain_stat('attack',2,dungeon.message_log)
            self.gain_stat('defense',2,dungeon.message_log)
            self.gain_stat('m_defense',2,dungeon.message_log)

        if 'loot' in monster.tags:
            self.make_item(random.randint(1, 2), dungeon.message_log)
        elif random.randint(1, 2) == 1:
            self.make_item(1, dungeon.message_log)

    def dungeon_tick(self, dungeon):
        if not self.in_combat and self.hp < self.max_hp:
            if self.next_regen:
                self.next_regen -= 1
            if self.next_regen <= 0:
                self.next_regen = self.regen_delay
                self.gain_hp(self.regen_amount)

@event.on('setup')
def on_setup():
    import main
    global stat_display
    global active_hero

    active_hero = Hero()

    stat_display = StatDisplay(
        width=main.sidebar_width,
        x=main.screen_width - main.sidebar_width,
        height=main.screen_height,
        draw_right=False, border_fg=pytality.colors.LIGHTGREY,
    )
