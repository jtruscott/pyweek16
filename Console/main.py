import pytality
import event
import game
import sys
import logging

log = logging.getLogger(__name__)
log.debug("Starting up")

screen_width = 100
screen_height = 80

def main():
    # For compatability reasons, i'm going to force pytality to be SDL only  for this compo.
    pytality.term.init(backends=['pygame'], width=screen_width, height=screen_height)
    
    pytality.term.set_title('No Title Yet (PyWeek #16)')
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
