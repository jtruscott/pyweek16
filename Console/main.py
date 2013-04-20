import pytality
import event
import game
import sys
import traceback
import logging
import sound

log = logging.getLogger(__name__)
log.debug("Starting up")

# At least one user on the IRC is at 1280x800, which with 12px tall rows limits us to 65 max.
screen_width = 155
screen_height = 65
sidebar_width = 26

def main():
    # For compatability reasons, i'm going to force pytality to be SDL only for this compo.
    pytality.term.init(backends=['pygame'], width=screen_width, height=screen_height)

    pytality.term.set_title('...As Was Foretold (PyWeek #16)')
    pytality.term.set_cursor_type(2)
    pytality.term.clear()

    if '--no-sound' in sys.argv:
        sys.argv.remove('--no-sound')
        sound.no_sound = True

    if 'load-image' in sys.argv:
        # hack to view images easily
        import time
        import os
        import pygame
        while True:
            print "Updating"
            with open(sys.argv[-1]) as f:
                buf = pytality.ansi.read_to_buffer(f, width=80, crop=False)
            pytality.term.clear()
            buf.draw()
            pytality.term.flip()
            mtime = new_mtime = os.stat(sys.argv[-1]).st_mtime
            while new_mtime == mtime:
                if pygame.event.peek(pygame.locals.QUIT):
                    sys.exit(0)
                pygame.event.pump()
                time.sleep(0.1)
                new_mtime = os.stat(sys.argv[-1]).st_mtime

    if 'test' in sys.argv:
        sys.argv.remove('test')
        import importlib
        import unittest
        unittest.main(importlib.import_module('Console.%s' % sys.argv[-1]), argv=['Test'])

    try:
        event.fire('setup')
        game.start()

    except game.GameShutdown:
        pytality.term.clear()

    except KeyboardInterrupt:
        pytality.term.clear()
        raise
    except Exception, e:
        log.exception(e)
        traceback.print_exc(e, file=sys.stderr)
        raise

    finally:
        log.debug('Shutting down')
        logging.shutdown()
        pytality.term.reset()
        if game.tick_thread:
            game.shutdown_event.set()
            # it really doesn't matter that we join these, it just suppresses errors
            game.tick_thread.join(timeout=0.1)
            game.input_thread.join(timeout=0.1)
