import pytality
import event
import game
import sys
import logging

log = logging.getLogger(__name__)
log.debug("Starting up")

# At least one user on the IRC is at 1280x800, which with 12px tall rows limits us to 65 max.
screen_width = 155
screen_height = 65

def main():
    # For compatability reasons, i'm going to force pytality to be SDL only for this compo.
    pytality.term.init(backends=['pygame'], width=screen_width, height=screen_height)
    
    pytality.term.set_title('No Title Yet (PyWeek #16)')
    pytality.term.set_cursor_type(2)
    pytality.term.clear()
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
