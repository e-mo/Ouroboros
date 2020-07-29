# s_manager.py
import logging
import threading
import asyncio
import concurrent.futures
import websockets
import hashlib
from functools import partial 

import q_manager
from session_pass import session_pass

async def start_session(uname, pwd):
    await __instance.start_session(uname, pwd)

async def end_session(sid):
    await __instance.end_session(sid)

class SessionManager:
    MAX_SESSIONS = 10;
    open_sessions = 0;
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.__instance.sessions = {}
        return cls.__instance

    async def start_session(self, uname, pwd):
        logging.info('"%s" starting session' % uname)
        if self.open_sessions >= self.MAX_SESSIONS:
            logging.warning('MAX_SESSIONS reached. Session creation aborted')
            return
        session = self.__Session(uname, pwd)

        self.open_sessions += 1
        self.sessions[uname] = session
        await session.start()
        del self.sessions[uname]
        self.open_sessions -= 1

    async def end_session(self, sid):
        logging.info('"%s" ending session' % sid)
        await self.sessions[sid].close()

    class __Session:
        URI = "ws://game.eternalcitygame.com:8080/tec"
        CLIENT_STRING = 'SKOTOS Orchil 0.2.3'
        closing = False
        
        def __init__(self, uname, pwd):
            self.send_key = ('%s_send' % uname)
            self.recv_key = ('%s_recv' % uname)
            self.uname  = uname
            self.pwd = pwd

        async def start(self):
            if await self.fetch_session_pass():
                if self.pwd == None:
                    logging.error(
                       '"%s" no session pass returned' % self.uname)
                else:
                    await self.websocket_start()

            logging.info('"%s" session ended' % self.uname)

        async def fetch_session_pass(self):
            logging.info('"%s" fetching session pass' % self.uname)

            executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=1)
            loop = asyncio.get_running_loop()

            try:
                self.pwd = await loop.run_in_executor(
                    executor, 
                    partial(session_pass, self.uname, self.pwd))
                return 1
            except:
                logging.error('"%s" unable to fetch session pass' % self.uname)
                self.raise_exception()

        async def websocket_start(self):
            logging.info('"%s" opening websocket' % self.uname)
            try:
                self.ws = await websockets.connect(self.URI)
            except:
                logging.error(
                        '"%s" unable to open websocket' % self.uname)
                self.raise_exception()
                self.close()
            else:
                logging.info('"%s" creating IO worker tasks' % self.uname)
                await asyncio.gather(self.websocket_recv(), self.websocket_send())
                 
        async def websocket_send(self):
            q_manager.put(self.send_key, self.CLIENT_STRING)

            def websocket_send_get():
                return q_manager.get(self.send_key)
            
            executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=1)
            loop = asyncio.get_running_loop()
            while True:
                msg = await loop.run_in_executor(
                    executor, 
                    websocket_send_get)

                if msg == q_manager.KILL: 
                    if not self.closing: await self.close()
                    logging.info('"%s" send task stopped' % self.uname)
                    break

                msg = ('%s\n' % msg).encode()
                await self.ws.send(msg)
                logging.info('"%s" sending \'%s\'' % (self.uname, msg))

        async def websocket_recv(self):
            while True:
                try:
                    msg = await self.ws.recv()
                except:
                    if not self.closing: await self.close()
                    logging.info('"%s" recv task stopped' % self.uname)
                    self.raise_exception()
                    break

                logging.info('"%s" recieved \'%s\'' % (self.uname, msg))
                q_manager.put(self.recv_key, msg)

        async def close(self):
            self.closing = True # No need to run this multiple times
            await self.close_ws()
            # Ensure all workers close
            q_manager.put(self.send_key, q_manager.KILL)
            q_manager.put(self.recv_key, q_manager.KILL)

        async def close_ws(self):
            try:
                await self.ws.close()
            except:
                self.raise_exception()

        def raise_exception(self):
            logging.debug('"%s" raised exception' % self.uname, exc_info=True)
            

            
__instance = SessionManager()

if __name__ == '__main__':
    import asyncio
    import sys

    logging.basicConfig(level=logging.INFO)
    async def test():
        if len(sys.argv) != 3:
            print('usage: s_manager.py UNAME PWD')
            exit()
        uname = sys.argv[1]
        pwd = sys.argv[2]
        q_manager.create_queue('%s_recv' % uname)
        q_manager.create_queue('%s_send' % uname)
        asyncio.create_task(start_session(uname, pwd))
        await asyncio.sleep(15)
        await end_session(uname)
        await asyncio.sleep(2)

    asyncio.run(test())
