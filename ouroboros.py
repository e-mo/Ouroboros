import threading
import logging

import io_thread
import gui
import q_manager

def configure_logger():
    format_str = '\
%(asctime)s %(filename)s %(funcName)s\n\
%(levelname)-7s %(message)s'
    logging.basicConfig(format=format_str, level=logging.INFO)

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
    q_manager.put_all(q_manager.KILL)
    logging.info('Goodbye!')
    iot.join()

if __name__ == '__main__':
    main()
