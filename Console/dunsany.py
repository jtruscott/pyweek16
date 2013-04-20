import pytality
import main
import event
import data
import time
import unittest

class PretentiousPullQuote(object):
    def __init__(self):
        start = 20

        def line(text, y):
            return pytality.buffer.PlainText(text, y=start + y, center_to=main.screen_width, fg=pytality.colors.BLACK)

        lines = [
            line("It had been prophecied that he should come there.", y=0),
            line("They knew it when the pebbles were being made", y=4),
            line("and before the isles of coral were given unto the sea.", y=8),
            line("And thus the prophecy came unto fulfilment and passed into history...", y=12),
            line("                                                       - Lord Dunsany", y=16),
        ]
        self.i = 0

        color_set = (pytality.colors.DARKGREY, pytality.colors.LIGHTGREY, pytality.colors.WHITE)
        self.stages = []
        at_i = 5
        for line in lines:
            for color in color_set:
                self.stages.append((at_i, line, color))
                at_i += 3
            at_i += 40

        at_i += 15 * 7
        self.visible_i = at_i

        for color in (pytality.colors.LIGHTGREY, pytality.colors.DARKGREY, pytality.colors.BLACK):
            for line in lines:
                self.stages.append((at_i, line, color))
            at_i += 7

        self.end = at_i + 7
        self.fire_end = None

        self.title_tl_bg = data.load_buffer("itsfullofstars.ans", width=22, crop=True)
        self.title_tr_bg = data.load_buffer("itsfullofstars.ans", width=22, crop=True)
        self.title_tl = data.load_buffer("aswasforet1b-1.ans", width=80, crop=False)
        self.title_tr = data.load_buffer("aswasforet1b-2.ans", width=42, crop=True)
        self.title_bl = data.load_buffer("town1b-1.ans", width=80, crop=False)
        self.title_br = data.load_buffer("town1b-2.ans", width=75, crop=True)

        self.title_bl_fire = data.load_buffer("town1b-1fire.ans", width=80, crop=False)
        self.title_br_fire = data.load_buffer("town1b-2fire.ans", width=75, crop=True)
        self.title_tl.x = 15
        self.title_tr.x = 80 + 15
        self.title_tr_bg.x = main.screen_width - 22

        self.title_bl.y = self.title_bl_fire.y = main.screen_height - self.title_br.height + 1
        self.title_br.y = self.title_br_fire.y = main.screen_height - self.title_br.height + 1
        self.title_br.x = self.title_br_fire.x = 80

        self.start_text = pytality.buffer.PlainText("[ Click To Start ]", fg=pytality.colors.WHITE, y=65 / 2)
        self.start_text.x = (main.screen_width - self.start_text.width) / 2

        self.credits_text = pytality.buffer.RichText(
            "<DARKGREY>  Game By: Jesse Truscott & Joe Gracyk" +
            "                     Art: Devin Vance" +
            "                     Writing: Dylan P??????" +
            "                     Music: Patashu "
        )

        self.root = pytality.buffer.Buffer(height=main.screen_height, width=main.screen_width, children=lines)

    def tick(self):
        if self.fire_end and self.i > self.fire_end:
                # and now fire adventure mode
                import game
                import adventure
                event.fire("adventure.setup")
                adventure.active_adventure.load_option("burn_1")
                game.mode = "adventure"

        if self.i > self.end:
            self.root.children = [
                self.title_tl_bg, self.title_tr_bg,
                self.title_tl, self.title_tr,
                self.title_bl, self.title_br,
                self.start_text, self.credits_text
            ]
            if self.fire_end:
                self.root.children += [self.title_bl_fire, self.title_br_fire]

            if self.i % 15 == 7:
                self.start_text.fg = pytality.colors.WHITE
                self.start_text.update_data()
            elif self.i % 15 == 0:
                self.start_text.fg = pytality.colors.LIGHTGREY
                self.start_text.update_data()
                self.root.dirty = True

        self.i += 1
        while self.stages and self.i >= self.stages[0][0]:
            i, line, color = self.stages.pop(0)
            line.fg = color
            line.update_data()

    def force_finish(self):
        if self.i < self.visible_i:
            self.i = self.visible_i
        elif self.i < self.end:
            self.i = self.end
        else:
            if not self.fire_end:
                # set the town on fire
                self.start_text.set("    Starting...   ")
                self.fire_end = self.i + 15

            else:
                self.i = self.fire_end

        self.tick()

    def draw(self):
        self.root.draw()

active_quote = None

@event.on("dunsany.setup")
def dunsany_setup():
    global active_quote
    active_quote = PretentiousPullQuote()


@event.on("dunsany.tick")
def dunsany_tick():
    active_quote.tick()

@event.on("dunsany.mouse_down")
def dunsany_mouse_down(x, y):
    active_quote.force_finish()

@event.on("dunsany.key")
def dunsany_key(key):
    if key == "enter" or key == " " or key == "\x1B":
        active_quote.force_finish()


@event.on("dunsany.draw")
def dunsany_draw():
    active_quote.draw()


class Test(unittest.TestCase):
    def test_run(self):
        import game
        event.fire("dunsany.setup")
        game.mode = "dunsany"
        game.start()
