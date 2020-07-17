import asyncio
import tkinter as tk
import time

async def foo(q):
    while True:
        print(await q.get())

        
async def bar(q):
    i = 0
    while True:
        await asyncio.sleep(2)
        await q.put('meow' + str(i))
        i += 1
        

async def main():
    q = asyncio.Queue()
    stuff = await asyncio.gather(foo(q), bar(q))
    print(stuff)
        

if __name__ == "__main__":
    asyncio.run(main())
