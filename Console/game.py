import event
import time
import pytality
import Queue as queue
import os
import threading
import traceback
import sys
import logging

log = logging.getLogger(__name__)

class GameShutdown(Exception):
    pass

Stop = object()

ticks = 0
target_fps = 15

# in previous compos i'd just take a lock and run stuff on the tick thread
# this time i'm going to try pushing stuff onto a queue so I can maybe make unit tests
action_queue = queue.Queue()
tick_thread = None
shutdown_event = threading.Event()

mode = "level"

def start():
    log.debug("Starting Game")

    global tick_thread
    tick_thread = threading.Thread(target=tick_loop, name="tick_loop")
    tick_thread.daemon = True
    tick_thread.start()

    global input_thread
    input_thread = threading.Thread(target=input_loop, name="input_loop")
    input_thread.daemon = True
    input_thread.start()

    try:
        while True:
            kwargs = action_queue.get()
            if kwargs is Stop:
                raise GameShutdown()

            event_name = kwargs.pop('type')
            if event_name == 'mouse_motion':
                pytality.term.move_cursor(**kwargs)

            event.fire('%s.%s' % (mode, event_name), **kwargs)
            event.fire('%s.predraw' % mode)
            event.fire('%s.draw' % mode)
            pytality.term.flip()

    except KeyboardInterrupt as e:
        raise GameShutdown()


def tick_loop():
    global ticks
    delay = 1.0 / target_fps
    try:
        log.debug("Tick thread started")
        while True:
            action_queue.put(dict(type='tick'))
            ticks += 1

            if shutdown_event.wait(delay):
                #we've been asked to shut dow
                log.debug("Tick thread shutting down")
                return
    
    except KeyboardInterrupt as e:
        action_queue.put(Stop)

    except Exception as e:
        logging.exception(e)
        try:
            traceback.print_exc(e, file=sys.stderr)
        finally:
            os._exit(1)
            return

def input_loop():
    try:
        log.debug("Input thread started")
        cursor_x = None
        cursor_y = None
        while True:
            k = pytality.term.getkey()
            if shutdown_event.is_set():
                log.debug("Tick thread shutting down")
                return

            if k:
                if type(k) is tuple:
                    # this is a mouse event
                    action, x, y = k
                    if action == 'mouse_motion' and x == cursor_x and y == cursor_y:
                        # throw it away if there's no "real" movement
                        continue
                    cursor_x = x
                    cursor_y = y
                    action_queue.put(dict(type=action, x=x, y=y))
                else:
                    action_queue.put(dict(type='key', key=k.lower()))

    except KeyboardInterrupt as e:
        action_queue.put(Stop)

    except Exception as e:
        logging.exception(e)
        try:
            traceback.print_exc(e, file=sys.stderr)
        finally:
            os._exit(1)
            return
