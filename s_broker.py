# s_broker.py
import asyncio
import threading
import logging

import s_manager
import q_manager
import m_server

BROKER_KEY = __name__
START = 'start'
END = 'end'
KILL = 'kill'

async def start_broker():
    await broker_task()

async def broker_task():
    logging.info('broker task starting')
    loop = asyncio.get_running_loop()
    task_list = []

    def session_broker_get():
        return q_manager.get(BROKER_KEY)

    while True:
        msg = await loop.run_in_executor(
                None, # Run in default executor
                session_broker_get)

        args = msg.split()

        if args[0] == START: 
            task_list.append(
                asyncio.create_task(s_manager.start_session(args[1], args[2])))
        elif args[0] == END:
            task_list.append(
                asyncio.create_task(s_manager.end_session(args[1])))
            task_list.append(
                asyncio.create_task(m_server.end_distribution(args[1])))
        elif args[0] == KILL:
            task_list.append(
                asyncio.create_task(s_manager.end_all()))
            task_list.append(
                asyncio.create_task(m_server.end_all()))

            await asyncio.gather(*task_list)
            break
            
    logging.info('broker task stopped')

def send_msg(broker_arg, *args):
    if len(args) in range(0, 4):
        msg = broker_arg
        for arg in args:
            msg += ' %s' % arg

        q_manager.put(BROKER_KEY, msg)
    else:
        logging.warning('incorrect number of args %s' % str(args))
