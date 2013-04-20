import os
import collections
import pytality
from room import Room, Level
import random
import logging
import data
import main
import hero
import message
import monsters
import event
import sound

log = logging.getLogger(__name__)

room_map = collections.defaultdict(list)
for file_name in os.listdir(data.data_dir):
    if 'room-' in file_name and '.ans' in file_name:
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
def generate_level(size, **kwargs):
    log.debug("Generating level")
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
        entrance_direction, dx, dy = next_deltas[exit_direction]
        x += dx
        y += dy

        walled_directions = set()
        for direction, (_, dx, dy) in next_deltas.iteritems():
            if (x + dx, y + dy) in rooms and direction != entrance_direction:
                walled_directions.add(direction)

        choices = []
        for key in room_map:
            if entrance_direction in key and len(key) > 1 and not key.intersection(walled_directions).difference(entrance_direction):
                choices.extend(room_map[key])

        if i == room_count - 1 or not choices:
            # this is the last room
            choice = random.choice(room_map[frozenset(entrance_direction)])
            done = True
            exit_direction = None

        else:
            choice = random.choice(choices)
            exit_direction = choice.directions.replace(entrance_direction, '')

        log.debug("chose room %r at x %r y %r", choice, x, y)
        rooms[(x, y)] = choice
        room_list.append((choice, x, y, entrance_direction))

        if done:
            break

    log.debug("Done! room_list=%r", room_list)

    return Level(rooms, room_list, **kwargs)

class Dungeon(object):
    def __init__(self, monster_type):
        sidebar_width = 26
        bottom_height = 17
        self.message_log = message.MessageLog(
            width=sidebar_width,
            height=main.screen_height,
            draw_left=False, border_fg=pytality.colors.LIGHTGREY,
        )
        self.stat_display = hero.stat_display
        self.stat_display.set_mode("dungeon")

        self.card_display = monsters.CardDisplay(
            width=main.screen_width - sidebar_width * 2,
            height=bottom_height,
            x=sidebar_width,
            y=main.screen_height - bottom_height,
            border_fg=pytality.colors.LIGHTGREY,
            dungeon=self,
            monster_type=monster_type
        )
        self.level = generate_level(
            10,
            x=sidebar_width,
            width=main.screen_width - sidebar_width * 2,
            height=main.screen_height - self.card_display.height
        )
        self.root = pytality.buffer.Buffer(height=0, width=0, children=[
            self.stat_display,
            self.message_log,
            self.card_display,
            self.level
        ])
        self.i = 0
        self.message_log.add("The hero sets out.")

    def tick(self):
        self.i += 1
        if self.i % 15 == 0:
            # safety margin
            self.root.dirty = True

        self.card_display.tick()
        self.level.tick(self)
        hero.active_hero.dungeon_tick(self)
        self.stat_display.tick(self)


    def draw(self):
        self.root.draw()

active_dungeon = None

@event.on("dungeon.setup")
def dungeon_setup(monster_type=None):
    global active_dungeon
    active_dungeon = Dungeon(monster_type=monster_type)
    sound.play_music("Curse_of_The_Patashu.mp3")

@event.on("dungeon.tick")
def dungeon_tick():
    active_dungeon.tick()

@event.on("dungeon.draw")
def dungeon_draw():
    active_dungeon.draw()


import unittest
class Test(unittest.TestCase):
    def test_mode(self):
        import game
        event.fire("setup")
        event.fire("dungeon.setup")
        hero.active_hero.has_sword = True
        hero.active_hero.has_shield = True

        game.mode = "dungeon"
        game.start(nosetup=True)

    def skip_test_generate(self):
        level = generate_level(10, width=100, height=60)
        self.assertTrue(level)

        for i, (x, y) in enumerate(level.move_path):
            level.main_buf._data[y][x] = [[8, 7, 15][(i/10) % 3], 0, '1234567890'[i%10]]
            level.view_buffer.view_x = (x - 40)
            level.view_buffer.view_y = (y - 40)
            level.view_buffer.draw()
            pytality.term.flip()
