import pytality
import random


class Overlay(pytality.buffer.Buffer):
    def __init__(self, **kwargs):
        self.animation = None
        super(Overlay, self).__init__(is_overlay=True, is_invisible=True, **kwargs)


    def start(self, anim_type, anim_speed=64, owner=None, color=None):
        self.animation = anim_type
        self.is_invisible = False
        self.empty_cells = set()
        self.fading_cells = set()
        self.faded_cells = set()
        self.anim_speed = anim_speed
        self.color = color
        self.i = 0
        for x in range(self.width):
            for y in range(self.height):
                if anim_type == "fade_out":
                    self._data[y][x][2] = ' '
                    self.empty_cells.add((y, x))

                elif anim_type == "fade_in":
                    self._data[y][x][2] = '\xDB'
                    self.empty_cells.add((y, x))

                elif anim_type == "flash":
                    self._data[y][x][2] = ' '
                    if y < owner.height and x < owner.width and not (owner._data[y][x][2] == ' ' and owner._data[y][x][1] == pytality.colors.BLACK):
                        self.empty_cells.add((y, x))


    def pick_and_move(self, source, cell, destination=None, qty=None):
        if source:
            if qty == all:
                spots = list(source)
            else:
                spots = random.sample(source, min(self.anim_speed, len((source))))
            for y, x in spots:
                self._data[y][x] = cell[:]
                if destination is not None:
                    destination.add((y, x))
            source.difference_update(spots)

    def tick(self, owner=None):
        if self.animation:
            owner.dirty = True
            self.dirty = True
            self.i += 1

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

        if self.animation == "flash":
            if self.color:
                color = self.color
            else:
                color = pytality.colors.WHITE

            if self.empty_cells and self.i == 1 or self.i == 5:
                self.pick_and_move(source=self.empty_cells, destination=self.fading_cells, cell=[color, pytality.colors.BLACK, '\xDB'], qty=all)

            if self.fading_cells and self.i == 3 or self.i == 6:
                self.pick_and_move(source=self.fading_cells, destination=self.empty_cells, cell=[color, pytality.colors.BLACK, ' '], qty=all)

            if self.i >= 6:
                self.animation = None
