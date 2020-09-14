# m_server.py
import asyncio
import logging
import queue

import q_manager

KILL = 'kill'

async def distribute(session, parsed_msg):
    await __instance.distribute(session, parsed_msg)

def subscribe(subscriber):
    __instance.subscribe(subscriber)
    
def unsubscribe(subscriber):
    __instance.unsubscribe(subscriber)

async def end_distribution(session):
    await __instance.end_distribution(session)

async def end_all():
    await __instance.end_all()


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

    def subscribe(self, subscriber):
        self.ensure_distributor(subscriber.session)
        self.distributors[subscriber.session].subscribe(subscriber)

    def unsubscribe(self, subscriber):
        self.distributors[subscriber.session].unsubscribe(subscriber)

    async def end_distribution(self, session):
        if session in self.distributors:
            logging.info('"%s" ending distribution' % session)
            await self.distributors[session].end()
            del self.distributors[session]
        else: 
            logging.warning('no "%s" distributor' % session)

    async def end_all(self):
        logging.info('ending all distribution')
        for session in list(self.distributors):
            await self.end_distribution(session)

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

        for m_type, msg in parsed_msg.items():
            await self.ensure_queue(m_type)
            await self.queues[m_type].put(msg)

    async def end(self):
        for queue in self.queues.values():
            await queue.put(KILL)

    async def ensure_queue(self, m_type):
        if m_type not in self.queues:
            logging.info('"%s" creating %s queue and distribution task'
                % (self.session, m_type))
            self.queues[m_type] = asyncio.Queue()
            self.start_dist_task(m_type)

    def start_dist_task(self, m_type):
        return asyncio.create_task(self.distribution_task(m_type))

    async def distribution_task(self, m_type):
        while True:
            msg = await self.queues[m_type].get()

            if msg == q_manager.KILL:
                break

            await self.distribute_msg(msg, m_type)
            
        logging.info('"%s" %s distribution task stopped'
            % (self.session, m_type))

    async def distribute_msg(self, msg, m_type):
        self.ensure_subscribers(m_type)
        if self.subscribers[m_type]:
            self.flush_backlog(m_type)
            for subscriber in self.subscribers[m_type]:
                await self.send_msg(subscriber, msg)
        elif msg is not q_manager.KILL:
            self.backlog_msg(msg, m_type)

    def backlog_msg(self, msg, m_type):
        logging.info(
            '"%s" no subscribers to %s. BACKLOGGING \'%s\''
            % (self.session, m_type, msg))
        self.ensure_backlog(m_type)
        self.backlogs[m_type].put(msg)

    def ensure_backlog(self, m_type):
        if m_type not in self.backlogs:
            logging.info('"%s" creating %s backlog' % (self.session, m_type))
            self.backlogs[m_type] = queue.Queue()

    async def send_msg(self, subscriber, msg):
        logging.info('"%s" sending \'%s\' -> \'%s\''
            % (self.session, msg, id(subscriber)))
        subscriber.send(msg)

    def q_key(self, sub_id):
        return '%s %s' % (self.session, sub_id)

    def subscribe(self, subscriber):
        self.ensure_subscribers(subscriber.m_type)

        logging.info('"%s" received new %s subscriber \'%s\''
            % (self.session, subscriber.m_type, id(subscriber)))
        self.subscribers[subscriber.m_type].append(subscriber)

        
    def unsubscribe(self, subscriber):
        self.ensure_subscribers(subscriber.m_type)
        if subscriber in self.subscribers[subscriber.m_type]:
            logging.info('"%s" removed %s subscriber \'%s\''
                % (self.session, subscriber.m_type, id(subscriber)))
            self.subscribers[subscriber.m_type].remove(subscriber) 
        else:
            logging.warning('"%s" no %s subscriber \'%s\''
                % (self.session, subscriber.m_type, id(subscriber)))

    def ensure_subscribers(self, m_type):
        if m_type not in self.subscribers:
            logging.info('"%s" creating %s subscribers list' 
                % (self.session, m_type))
            self.subscribers[m_type] = []

    def flush_backlog(self, m_type):
        self.ensure_backlog(m_type)

        while not self.backlogs[m_type].empty():
            msg = self.backlogs[m_type].get()
            logging.info('"%s" flushing %s from backlog'
                % (self.session, msg))
            self.queues[m_type].put_nowait(msg)

__instance = MessageServer()
