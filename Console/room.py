import pytality
import heapq

room_size = 40

#http://stackoverflow.com/questions/4159331/python-speed-up-an-a-star-pathfinding-algorithm
def a_star(current, end, tiles):

    openSet = set()
    openHeap = []
    closedSet = set()

    #cutoff the path ends
    current.parent = None
    current.G = 0
    current.H = 0
    end.parent = None

    def retrace_path(c):
        path = [c]
        while c.parent is not None:
            c = c.parent
            path.append(c)
        path.reverse()
        return path

    def neighbors(tile):
        x = tile.x
        y = tile.y
        if x > 0:
            yield tiles[y][x-1]
        if x+1 < room_size:
            yield tiles[y][x+1]
        if y > 0:
            yield tiles[y-1][x]
        if y+1 < room_size:
            yield tiles[y+1][x]

    openSet.add(current)
    openHeap.append((0, current))
    while openSet:
        current = heapq.heappop(openHeap)[1]
        if current == end:
            return retrace_path(current)
        openSet.remove(current)
        closedSet.add(current)
        for tile in neighbors(current):
            if tile.char == '\xDB':
                continue

            if tile not in closedSet:

                G = current.G + 1
                tile.H = (abs(end.x-tile.x) + abs(end.y-tile.y))

                if tile not in openSet or G < tile.G:
                    tile.G = G
                    tile.F = tile.G + tile.H
                    tile.parent = current

                if tile not in openSet:
                    openSet.add(tile)
                    heapq.heappush(openHeap, (tile.F, tile))
    return []


endpoint_map = dict(
    n=(19, 0),
    s=(19, 39),
    e=(39, 19),
    w=(0, 19),
)

class Tile(object):
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char

    def __repr__(self):
        return '<Tile x=%r, y=%r, c=%r>' % (self.x, self.y, self.char)


class Room(object):
    def __init__(self, buf, directions, file_name):
        self.buf = buf
        self.directions = directions
        self.file_name = file_name
        self.routes = {}

        self.load_buf()

    def load_buf(self):
        tiles = []
        x_tile = None
        for y, row in enumerate(self.buf._data[:room_size]):
            tile_row = []
            for x, cell in enumerate(row[:room_size]):
                fg, bg, char = cell
                tile = Tile(x=x, y=y, char=char)
                tile_row.append(tile)
                if char == 'X':
                    x_tile = tile
            tiles.append(tile_row)
        return tiles, x_tile

    def path_from(self, source):
        if source in self.routes:
            return self.routes[source]

        #we need a new one on each pass.
        tiles, x_tile = self.load_buf()

        if not source:
            # we want a path from the X
            # which means we have only one exit
            start_x, start_y = x_tile.x, x_tile.y
            destination = self.directions
        else:
            start_x, start_y = endpoint_map[source]
            destination = self.directions.replace(source, '')

        if not destination:
            # we only have one entrance
            # so we want a path to the X
            end_x, end_y = x_tile.x, x_tile.y
        else:
            end_x, end_y = endpoint_map[destination]

        route = a_star(tiles[start_y][start_x], tiles[end_y][end_x], tiles)
        self.routes[source] = route
        return route

    def __repr__(self):
        return '<Room name="%s" directions="%s">' % (self.file_name, self.directions)


class Level(pytality.buffer.Buffer):
    def __init__(self, room_map, room_list, **kwargs):
        super(Level, self).__init__(**kwargs)
        min_x = max_x = min_y = max_y = 0
        for x, y in room_map:
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)

        self.main_buf = pytality.buffer.Buffer(
            width=room_size * (1 + max_x - min_x) + 20,
            height=room_size * (1 + max_y - min_y) + 20,
        )
        self.move_path = []

        for room, room_x, room_y, entrance_direction in room_list:
            start_x = room_size * (room_x - min_x) + 10
            start_y = room_size * (room_y - min_y) + 10

            for y, row in enumerate(room.buf._data[:room_size]):
                for x, cell in enumerate(row[:room_size]):
                    fg, bg, char = cell
                    if fg == pytality.colors.BLACK and bg == pytality.colors.BLACK and char == ' ':
                        continue

                    self.main_buf._data[start_y + y][start_x + x] = [fg, bg, char]

                    if char == 'X' and (room_x, room_y) == (0, 0):
                        self.begin_location = start_x + x, start_y + y
                    else:
                        self.end_location = start_x + x, start_y + y

            for tile in room.path_from(entrance_direction):
                x = tile.x + start_x
                y = tile.y + start_y
                self.move_path.append((x, y))

        self.view_buffer = pytality.buffer.BufferView(parent=self.main_buf, width=self.width, height=self.height)
        self.hero_sprite = pytality.buffer.PlainText("\x01", fg=pytality.colors.WHITE)
        self.hero_location = self.begin_location
        self.children = [self.view_buffer, self.hero_sprite]

    def tick(self):
        if self.move_path:
            self.hero_location = self.move_path.pop(0)
            self.center_map_on_hero()

    def center_map_on_hero(self):
        map_x, map_y = self.hero_location
        self.view_buffer._view_x = max(0, map_x - (self.view_buffer.width / 2))
        self.view_buffer._view_y = max(0, map_y - (self.view_buffer.height / 2))
        self.hero_sprite.x = (map_x - self.view_buffer._view_x)
        self.hero_sprite.y = (map_y - self.view_buffer._view_y)
        self.dirty = True

import unittest
class Test(unittest.TestCase):
    def test_pathing(self):
        for room_type in room_map.values():
            for room in room_type:
                print 'room:', room
                for c in room.directions:
                    route = room.path_from(c)
                    for i, tile in enumerate(route):
                        room.buf._data[tile.y][tile.x] = [[0, 8, 7, 15][i % 4], 0, '*']
                room.buf.draw()
                pytality.term.flip()
                while pytality.term.getkey() != 'n':
                    continue
