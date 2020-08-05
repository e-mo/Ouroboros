# m_server.py
import asyncio
import logging
import queue

import q_manager

async def distribute(session, parsed_msg):
    await __instance.distribute(session, parsed_msg)

async def subscribe(sub_id, session, msg_type):
    await __instance.subscribe(sub_id, session, msg_type)

class MessageServer:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.__instance.distributors = {}
        return cls.__instance

    async def distribute(self, session, parsed_msg):
        self.ensure_distributor(session)
        await self.distributors[session].distribute(parsed_msg)

    async def subscribe(self, sub_id, session, msg_type):
        self.ensure_distributor(session)
        await self.distributors[session].subscribe(
            sub_id, msg_type)

    def ensure_distributor(self, session):
        if session not in self.distributors:
            logging.info('"%s" creating distributor' % session)
            self.distributors[session] = Distributor(session)


class Distributor:

    def __init__(self, session):
        self.session = session 
        self.queues = {}
        self.backlogs = {}
        self.subscribers = {}

    async def distribute(self, parsed_msg):
        logging.info('"%s" distributing sorted msg %s'
            % (self.session, str(parsed_msg))) 

        for msg_type, msg in parsed_msg.items():
            await self.ensure_queue(msg_type)
            await self.queues[msg_type].put(msg)

    async def ensure_queue(self, msg_type):
        if msg_type not in self.queues:
            logging.info('"%s" creating %s queue and distribution task'
                % (self.session, msg_type))
            self.queues[msg_type] = asyncio.Queue()
            self.backlogs[msg_type] = queue.Queue()
            self.start_dist_task(msg_type)

    def start_dist_task(self, msg_type):
        return asyncio.create_task(self.distribution_task(msg_type))

    async def distribution_task(self, msg_type):
        while True:
            msg = await self.queues[msg_type].get()
            try:
                for sub_id in self.subscribers[msg_type]:
                    logging.info('"%s" distributing \'%s\' -> \'%s\''
                        % (self.session, msg, sub_id))
                    q_key = ('%s%s%s' % (self.session, msg_type, sub_id))
                    q_manager.put(q_key, msg)
            except KeyError:
                logging.info(
                    '"%s" no subscribers to %s. Backlogging \'%s\''
                    % (self.session, msg_type, msg))
                self.backlogs[msg_type].put(msg)

    async def subscribe(self, sub_id, msg_type):
        if msg_type not in self.subscribers:
            logging.info('"%s" received new %s subscriber \'%s\''
                % (self.session, msg_type, sub_id))
            self.subscribers[msg_type] = [sub_id]
        else: self.subscribers[msg_type].append(sub_id)
        self.flush_backlog(sub_id, msg_type)

    async def backlog(self, msg_type, msg):
        logging.info('backlog found')
        await self.backlogs[msg_type].put(msg)

    def flush_backlog(self, sub_id, msg_type):
        q_key = ('%s%s%s' % (self.session, msg_type, sub_id))
        while not self.backlogs[msg_type].empty():
            msg = self.backlogs[msg_type].get()
            logging.info('"%s" flushing %s from backlog'
                % (self.session, msg))
            self.queues[msg_type].put_nowait(msg)

__instance = MessageServer()
