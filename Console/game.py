import event
import pytality
import logging

log = logging.getLogger(__name__)

class GameShutdown(Exception): pass

def start():
    log.debug("Starting Game")
    pytality.term.getkey()
