# m_server.py
import asyncio

async def distribute(session, sorted_msg):
    await __instance.distribute(session, sorted_msg)

async def subscribe(sub_id, session, msg_type):
    await __instance.subscribe(sub_id, session, msg_type)

class MessageServer:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.__instance.distributors = {}
        return cls.__instance

    async def distribute(self, session, sorted_msg):
        self.ensure_distributor(session)
        await self.distributors[session].distribute(sorted_msg)

    async def subscribe(self, sub_id, session, msg_type):
        self.ensure_distributor(session)
        await self.distributors[session].subscribe(
            sub_id, msg_type)

    def ensure_distributor(self, session):
        if session not in self.distributors:
            self.distributors[session] = self.__Distributor(session)


    class __Distributor:

        def __init__(self, session):
            self.session = session 
            self.queues = {}
            self.backlogs = {}
            self.subscribers = {}

        async def distribute(self, sorted_msg):
            for msg_type, msg in sorted_msg.items():
                await self.ensure_queue(msg_type)
                await self.queues[msg_type].put(msg)

        async def ensure_queue(self, msg_type):
            if msg_type not in self.queues:
                self.queues[msg_type] = asyncio.Queue()
                self.start_dist_task(msg_type)

        def start_dist_task(self, msg_type):
            return asyncio.create_task(self.distribution_task(msg_type))

        async def distribution_task(self, msg_type):
            while True:
                print(await self.queues[msg_type].get())
                if msg_type in self.subscribers:
                    print(*self.subscribers[msg_type])

        async def subscribe(self, sub_id, msg_type):
            if sub_id not in self.subscribers:
                self.subscribers[msg_type] = [sub_id]
            else: self.subscribers[msg_type].append(sub_id)
                
__instance = MessageServer()
