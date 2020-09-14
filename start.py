import logging

import io_thread
import gui

format_str = ('%(asctime)s %(filename)s %(funcName)s\n'
              '%(levelname)-7s %(message)s')
logging.basicConfig(
    format=format_str, 
    level=logging.INFO)

io_thread.start()
gui.main()
io_thread.end()

logging.info('Goodbye!')
