import pytality
import main
import event
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

        self.root = pytality.buffer.Buffer(height=main.screen_height, width=main.screen_width, children=lines + [self.title_l, self.title_r])

    def tick(self):
        if self.i > self.end:
            import game
            event.fire("dungeon.setup")
            game.mode = "dungeon"

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
    print repr(key)
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
