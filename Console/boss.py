import pytality
import event
import hero
import main
import overlay
import data
import random
import clickable
import time

class BattleSprite(pytality.buffer.Buffer):
    def __init__(self, width=16, height=16, crop=True, file_names=None, anim_delay = 5, **kwargs):
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
        real_boss = False
        if real_boss:
            self.boss_sprite = BattleSprite(file_names=["finalboss.ans"], width=61, height=48, x=self.battle_window.width - 61, y=0, crop=True)
        else:
            self.boss_sprite = BattleSprite(file_names=["you2.ans", "you2alt.ans"], width=34, height=31, x=self.battle_window.width - 40, y=14, crop=True)
        self.hero_sprite = BattleSprite(file_names=["herods.ans"], width=18, height=15, x=10, y=30)

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

    def tick(self):
        self.i += 1
        if self.i % 15 == 0:
            # safety margin
            self.root.dirty = True

        self.stat_display.tick(self)

        # wheeee let's be stupid
        #if self.i % 20 == 0:
        #    self.hero_sprite.overlay.start("fade_in")
        #if self.i % 20 == 10:
        #    self.boss_sprite.overlay.start("fade_in")

        # animation tickers
        self.hero_sprite.tick()
        self.boss_sprite.tick()

        # wheeee let's be stupid
        #if not self.boss_sprite.overlay.animation:
        #    self.boss_sprite.x = max(min(self.boss_sprite.x + random.randint(-1, 1), self.battle_window.width - 16), 0)
        #    self.boss_sprite.y = max(min(self.boss_sprite.y + random.randint(-1, 1), self.battle_window.height - 16), 0)
        #if not self.hero_sprite.overlay.animation:
        #    self.hero_sprite.x = max(min(self.hero_sprite.x + random.randint(-1, 1), self.battle_window.width - 16), 0)
        #    self.hero_sprite.y = max(min(self.hero_sprite.y + random.randint(-1, 1), self.battle_window.height - 16), 0)

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
