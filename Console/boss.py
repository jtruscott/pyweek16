import pytality
import event
import hero
import main
import overlay
import data
import random
import time

class BattleSprite(pytality.buffer.Buffer):
    def __init__(self, file_name=None, **kwargs):
        super(BattleSprite, self).__init__(width=16, height=16, **kwargs)
        self.sprite = data.load_buffer(file_name, width=14, crop=True)
        self.sprite.x = 1
        self.sprite.y = 1
        self.overlay = overlay.Overlay(width=16, height=16, x=0, y=0)
        self.children = [self.sprite, self.overlay]


class Battle(object):
    def __init__(self, dungeon):
        sidebar_width = 26
        bottom_height = 17

        self.message_log = dungeon.message_log
        self.stat_display = dungeon.stat_display
        self.stat_display.set_mode("battle")


        self.battle_window = pytality.buffer.Buffer(
            x=sidebar_width,
            y=0,
            height=main.screen_height - bottom_height,
            width=main.screen_width - (sidebar_width * 2)

        )
        self.boss_sprite = BattleSprite(file_name="idk.ans", x=10, y=10)
        self.hero_sprite = BattleSprite(file_name="pinata.ans", x=self.battle_window.width - 30, y=10)

        self.battle_window.children = [self.boss_sprite, self.hero_sprite]

        self.fullscreen_flash = pytality.buffer.Buffer(
            x=sidebar_width,
            height=main.screen_height,
            width=main.screen_width - (sidebar_width * 2)
        )

        self.root = pytality.buffer.Buffer(height=0, width=0, children=[
            self.message_log,
            self.stat_display,
            self.battle_window
        ])
        self.i = 0
        self.flashed = False
        self.message_log.add("\n     <LIGHTRED>BOSS BATTLE!")

    def tick(self):
        self.i += 1
        if self.i % 15 == 0:
            # safety margin
            self.root.dirty = True

        self.stat_display.tick(self)
        self.boss_sprite.x = max(min(self.boss_sprite.x + random.randint(-1, 1), self.battle_window.width - 16), 0)
        self.boss_sprite.y = max(min(self.boss_sprite.y + random.randint(-1, 1), self.battle_window.height - 16), 0)
        self.hero_sprite.x = max(min(self.hero_sprite.x + random.randint(-1, 1), self.battle_window.width - 16), 0)
        self.hero_sprite.y = max(min(self.hero_sprite.y + random.randint(-1, 1), self.battle_window.height - 16), 0)

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
            self.battle_window.draw()


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
        event.fire("dungeon.setup")
        game.mode = "boss"
        event.fire("boss.setup", dungeon.active_dungeon)
        game.start()
