# io_thread.py
import asyncio
import threading
import logging

import q_manager
import s_manager

async def session_broker():
    logging.info('session_broker starting')
    loop = asyncio.get_running_loop()
    queue_key = 'session_broker'
    q_manager.create_queue(queue_key)
    task_list = []

    def session_broker_get():
        return q_manager.get(queue_key)

    while True:
        msg = await loop.run_in_executor(
                None, # Run in default executor
                session_broker_get)

        if msg == q_manager.KILL: 
            await asyncio.gather(*task_list)
            logging.info('session_broker stopped')
            break

        args = msg.split()
        if args[0] == 'start': 
            task_list.append(
                asyncio.create_task(s_manager.start_session(args[1], args[2])))
        elif args[0] == 'end':
            asyncio.create_task(s_manager.end_session(args[1]))

async def start_io():
    await session_broker()
    logging.info('io_thread stopped')
    
def main():
    logging.info('io_thread starting')
    asyncio.run(start_io())
