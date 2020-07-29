# io_thread.py
import asyncio
import threading
import logging

import q_manager

async def session_broker():
    loop = asyncio.get_running_loop()
    queue_key = 'session_broker'
    q_manager.create_queue(queue_key)

    def session_broker_get():
        return q_manager.get(queue_key)

    while True:
        msg = await loop.run_in_executor(
                None, # Run in default executor
                session_broker_get)

        logging.debug(('Received "%s" from queue "%s"' % (msg, queue_key)))
        if msg == q_manager.KILL: 
            logging.info('Goodbye!')
            break

async def start_io():
    logging.info('Starting session_broker')
    await session_broker()
    logging.info('Goodbye!')
    
def main():
    asyncio.run(start_io()),
