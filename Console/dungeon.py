import os
import collections
import pytality
from room import Room, Level
import random
import logging
import data

log = logging.getLogger(__name__)

room_map = collections.defaultdict(list)
for file_name in os.listdir(data.data_dir):
    if 'room-' in file_name:
        prefix, directions, suffix = file_name.split('-', 2)
        room_buf = data.load_buffer(file_name, width=155, crop=True)
        room = Room(buf=room_buf, directions=directions, file_name=file_name)
        room_map[frozenset(directions)].append(room)

next_deltas = dict(
    n=('s', 0, -1),
    s=('n', 0, 1),
    w=('e', -1, 0),
    e=('w', 1, 0),
)
def generate_level(size):
    print 'room_map:', room_map
    start_room = random.choice(random.choice([room for key, room in room_map.iteritems() if len(key) == 1]))
    room_count = random.randint(size-2, size+2)
    x = 0
    y = 0
    rooms = {
        (x, y): start_room
    }
    room_list = [(start_room, 0, 0, None)]

    exit_direction = start_room.directions
    done = False
    for i in range(room_count):
        print 'i:', i
        entrance_direction, dx, dy = next_deltas[exit_direction]
        x += dx
        y += dy

        walled_directions = set()
        for direction, (_, dx, dy) in next_deltas.iteritems():
            if (x + dx, y + dy) in rooms and direction != entrance_direction:
                walled_directions.add(direction)

        print 'entrance_direction:', entrance_direction
        choices = []
        for key in room_map:
            if entrance_direction in key and len(key) > 1 and not key.intersection(walled_directions).difference(entrance_direction):
                choices.extend(room_map[key])

        print 'walled_directions:', walled_directions
        print 'choices:', choices
        if i == room_count - 1 or not choices:
            # this is the last room
            choice = random.choice(room_map[frozenset(entrance_direction)])
            done = True
            exit_direction = None
            end_room_location = (x, y)
        else:
            choice = random.choice(choices)
            exit_direction = choice.directions.replace(entrance_direction, '')

        print 'choice:', choice, choice.directions
        rooms[(x, y)] = choice
        room_list.append((choice, x, y, entrance_direction))

        if done:
            break

    print 'rooms:', rooms
    print 'room_list:', room_list
    print 'end:', end_room_location

    return Level(rooms, room_list)

import unittest
class Test(unittest.TestCase):
    def test_generate(self):
        level = generate_level(10)
        self.assertTrue(level)

        for i, (x, y) in enumerate(level.move_path):
            level.main_buf._data[y][x] = [[8, 7, 15][(i/10) % 3], 0, '1234567890'[i%10]]
            level.buf.view_x = (x - 40)
            level.buf.view_y = (y - 40)
            level.buf.draw()
            pytality.term.flip()
