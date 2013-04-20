import os
import pytality
import pygame
import event
import logging

log = logging.getLogger(__name__)

data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'music')

last_sound = None
no_sound = False

@event.on('setup')
def setup_sound():
    if no_sound:
        log.debug("not setting up sound")
        return

    log.debug("setting up sound")
    #witchcraft, this one
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()

def play(filename, queue=False, restart=False):
    if no_sound:
        return

    global last_sound
    if last_sound == filename and not restart:
        return

    log.debug("playing sound %r", filename)
    filename = os.path.join(data_dir, filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)
    last_sound = filename

import unittest
class Test(unittest.TestCase):
    def test_sound(self):
        import time
        setup_sound()
        #play('OHC_Changeling_Rumble.mp3')
        play('Catastrophe_Strikes.mp3')

        while pygame.mixer.music.get_busy():
            pytality.term.flip()
            pytality.term.getkey()
