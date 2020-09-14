# io_thread.py
import asyncio
import logging
import threading

import s_broker

async def start_io():
    await s_broker.start_broker()
    logging.info('io_thread stopped')
    
def main():
    logging.info('io_thread starting')
    asyncio.run(start_io())

def start():
    global IO_THREAD
    IO_THREAD = threading.Thread(
            target=main,
            args=(),
            daemon=True)
    IO_THREAD.start()

def end():
    s_broker.send_msg(s_broker.KILL)
    IO_THREAD.join()
