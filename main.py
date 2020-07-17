import asyncio
import websockets

async def recv(websocket, recv_queue):
    while True:
        msg = await websocket.recv()
        await recv_queue.put(msg)

async def consume(recv_queue):
    while True:
        msg = await recv_queue.get()
        print(msg)

def test(session):
    recv_queue = asyncio.Queue()
    recv_task = asyncio.create_task(recv(session, recv_queue))
    recv_consumer = asyncio.create_task(consume(recv_queue))
    

async def new_session():
    HOST = 'game.eternalcitygame.com'
    PORT = '8080'
    DIR = 'tec'
    uri = ("ws://%s:%s/%s" % (HOST, PORT, DIR))
    session = await websockets.connect(uri)
    return session

async def main():
    session = await new_session()
    await session.ping()
    test(session)




if __name__ == '__main__':
    asyncio.run(main())
