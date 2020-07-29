import asyncio
import websockets
import hashlib
import time

async def main():
    uri = "ws://game.eternalcitygame.com:8080/tec"
    async with websockets.connect(uri) as websocket:
        uname = b"moyalinka"
        passw = b"1161651636"
        secret = b"NONE"
        await websocket.send("SKOTOS Orchil 0.2.3\n")
        while True:
            message = await websocket.recv()
            if b"SECRET" in message:
                await websocket.send(b"USER " + uname + b"\n")
                await websocket.send(b"SECRET " + secret + b"\n")
                md5hash = hashlib.md5(uname + passw + secret)
                await websocket.send("HASH " + md5hash.hexdigest() + "\n")
            if b"SKOOT" in message:
                time.sleep(1)
                await websocket.send(b"play" + b"\n")
            if b"[1]" in message:
                await websocket.send(b"1" + b"\n")
            print(message.decode())

asyncio.get_event_loop().run_until_complete(main())
