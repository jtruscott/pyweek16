import pytality
import random


class Overlay(pytality.buffer.Buffer):
    def __init__(self, **kwargs):
        self.animation = None
        super(Overlay, self).__init__(is_overlay=True, is_invisible=True, **kwargs)


    def start(self, anim_type):
        self.animation = anim_type
        self.is_invisible = False
        self.empty_cells = set()
        self.fading_cells = set()
        self.faded_cells = set()
        for x in range(self.width):
            for y in range(self.height):
                if anim_type == "fade_out":
                    self._data[y][x][2] = ' '
                    self.empty_cells.add((y, x))

                elif anim_type == "fade_in":
                    self._data[y][x][2] = '\xDB'
                    self.empty_cells.add((y, x))

    def pick_and_move(self, source, cell, destination=None, qty=64):
        if source:
            spots = random.sample(source, min(qty, len((source))))
            for y, x in spots:
                self._data[y][x] = cell[:]
                if destination is not None:
                    destination.add((y, x))
            source.difference_update(spots)

    def tick(self, owner):
        if self.animation:
            owner.dirty = True
            self.dirty = True

        if self.animation == "fade_out":
            self.pick_and_move(source=self.faded_cells, cell=[pytality.colors.BLACK, pytality.colors.BLACK, '\xDB'])
            self.pick_and_move(source=self.fading_cells, destination=self.faded_cells, cell=[pytality.colors.DARKGREY, pytality.colors.BLACK, '\xB0'])
            self.pick_and_move(source=self.empty_cells, destination=self.fading_cells, cell=[pytality.colors.LIGHTGREY, pytality.colors.BLACK, '\xB1'])

            if not self.faded_cells and not self.fading_cells and not self.empty_cells:
                self.animation = None

        if self.animation == "fade_in":
            self.pick_and_move(source=self.faded_cells, cell=[pytality.colors.BLACK, pytality.colors.BLACK, ' '])
            self.pick_and_move(source=self.fading_cells, destination=self.faded_cells, cell=[pytality.colors.DARKGREY, pytality.colors.BLACK, '\xB1'])
            self.pick_and_move(source=self.empty_cells, destination=self.fading_cells, cell=[pytality.colors.LIGHTGREY, pytality.colors.BLACK, '\xB0'])

            if not self.faded_cells and not self.fading_cells and not self.empty_cells:
                self.animation = None

