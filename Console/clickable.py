import pytality
import main
import event
import logging

log = logging.getLogger(__name__)

buffers = set()
hovered = None

def register(buf):
    log.debug("registering %r", buf)
    buffers.add(buf)

def unregister(buf):
    log.debug("unregistering %r", buf)
    buffers.remove(buf)
    global hovered
    if buf == hovered:
        hovered = None

def unregister_all():
    global buffers
    global hovered
    buffers = set()
    hovered = None

def mouse_move(x, y):
    global hovered
    for buf in buffers:
        if (buf._x + buf.x_offset) <= x < (buf._x + buf.x_offset + buf.width) and (buf._y + buf.y_offset) <= y < (buf._y + buf.y_offset + buf.width):
            #print 'hovered', hovered, 'buf', buf
            if hovered != buf:
                if hovered:
                    hovered.mouse_out(x, y)
                hovered = buf
                buf.mouse_in(x, y)
            else:
                # while the cursor is over you, you need to redraw each pass
                # for slightly janky timing reasons, we want to draw _now_ so the
                # cursor replace functions get the right data.
                buf.dirty = True
            buf.draw(x_offset=buf.x_offset, y_offset=buf.y_offset)
            return

    if hovered:
        hovered.mouse_out(x, y)
        hovered = None

def mouse_down(x, y):
    for buf in buffers:
        if (buf._x + buf.x_offset) <= x < (buf._x + buf.x_offset + buf.width) and (buf._y + buf.y_offset) <= y < (buf._y + buf.y_offset + buf.width):
            buf.mouse_down(x, y)
            return

    log.debug("mouse_down: no target")


class ClickableBox(pytality.buffer.Box):
    def __init__(self,
            hover_interior_bg=pytality.colors.BLACK, hover_border_bg=pytality.colors.BLACK,
            hover_interior_fg=pytality.colors.WHITE, hover_border_fg=pytality.colors.WHITE,
            on_mouse_down=None,
            **kwargs):

        super(ClickableBox, self).__init__(**kwargs)
        kwargs.update(
            interior_bg=hover_interior_bg, border_bg=hover_border_bg,
            interior_fg=hover_interior_fg, border_fg=hover_border_fg,
        )
        self._regular_data = self._data
        self._hover_data = pytality.buffer.Box(**kwargs)._data
        self.on_mouse_down = on_mouse_down

    def mouse_in(self, x, y):
        #print 'in', self, x, y
        self._data = self._hover_data
        self.dirty = True

    def mouse_out(self, x, y):
        #print 'out', self, x, y
        self._data = self._regular_data
        self.dirty = True

    def mouse_down(self, x, y):
        #print 'down', self, x, y
        if self.on_mouse_down:
            self.on_mouse_down(self, x, y)




import unittest
class Test(unittest.TestCase):
    def test_buttons(self):
        import game
        game.mode = 'test'
        p = ClickableBox(x=10, y=20, width=10, height=5, border_fg=pytality.colors.DARKGREY)
        p2 = ClickableBox(x=20, y=20, width=5, height=5, border_fg=pytality.colors.DARKGREY, hover_border_bg=pytality.colors.WHITE)
        register(p)
        register(p2)

        def mouse_down(x, y):
            p2.mouse_out(x, y)
            unregister(p2)
        p2.mouse_down = mouse_down

        @event.on('test.draw')
        def on_draw():
            p.draw()
            p2.draw()

        game.start()

