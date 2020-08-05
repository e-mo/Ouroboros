# s_broker.py
import asyncio
import threading
import logging

import s_manager
import q_manager

import io_interface

BROKER_KEY = '60%s420' % __name__
START = 'start'
END = 'end'
START_MSG = ' %s %s'
END_MSG = '%s %s'

async def start_broker():
    logging.info('s_broker starting')
    loop = asyncio.get_running_loop()
    task_list = []
    io_interface.start_session('moyalinka', 'Morsee6294')

    def session_broker_get():
        return q_manager.get(BROKER_KEY)

    while True:
        msg = await loop.run_in_executor(
                None, # Run in default executor
                session_broker_get)

        if msg == q_manager.KILL: 
            await asyncio.gather(*task_list)
            logging.info('s_broker stopped')
            break

        args = msg.split()
        if args[0] == START: 
            task = asyncio.create_task(
                s_manager.start_session(args[1], args[2]))
            task_list.append(task)
        elif args[0] == END:
            asyncio.create_task(s_manager.end_session(args[1]))

def send_msg(broker_arg, *args):
    if len(args) in range(1, 3):
        msg = broker_arg
        for arg in args:
            msg += ' %s' % arg

        q_manager.put(BROKER_KEY, msg)
    else:
        logging.warning('incorrect number of args %s' % str(args))
