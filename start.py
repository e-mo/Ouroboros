import threading
import logging

import io_thread
import gui
import q_manager

def configure_logger():
    format_str = '\
%(asctime)s %(filename)s %(funcName)s\n\
%(levelname)-7s %(message)s'
    logging.basicConfig(format=format_str, level=logging.DEBUG)

def main():
    configure_logger()

    iot = threading.Thread(
            target=io_thread.main,
            args=(),
            daemon=True)
    iot.start()
    gui.main()

    # Tell all the consumer threads to stop. 
    logging.debug('Sending KILL message to all consumers')
    q_manager.kill_all() 
    iot.join()
    logging.info('Goodbye!')

if __name__ == '__main__':
    main()
