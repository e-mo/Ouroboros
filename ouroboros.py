import threading
import logging

import io_thread
import gui
import q_manager

def configure_logger():
    format_str = '\
%(asctime)s %(filename)-12s %(funcName)s\n\
%(levelname)-7s %(message)s'
    logging.basicConfig(format=format_str, level=logging.DEBUG)

def main():
    configure_logger()

    logging.info('Starting IO thread')
    iot = threading.Thread(
            target=io_thread.main,
            args=(),
            daemon=True)
    iot.start()
    logging.info('Starting GUI')
    gui.main()

    # Tell all the consumer threads to close. 
    logging.debug('Sending KILL message to all consumers')
    q_manager.put_all(q_manager.KILL)
    logging.info('Goodbye!')
    iot.join()

if __name__ == '__main__':
    main()
