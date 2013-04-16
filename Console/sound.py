import os
import collections
import pytality
from room import Room, Level
import random
import logging
import threading
import pygame

log = logging.getLogger(__name__)

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'music')

def setup():
    #witchcraft, this one
    pygame.mixer.pre_init(44100,-16,2, 1024)
    pygame.mixer.init()

def play(filename, queue=False):
    filename = os.path.join(data_dir, filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)

import unittest
class Test(unittest.TestCase):
    def test_sound(self):
        import time
        setup()
        #play('OHC_Changeling_Rumble.mp3')
        play('Catastrophe_Strikes.mp3')

        while pygame.mixer.music.get_busy():
            pytality.term.flip()
        time.sleep(2)
