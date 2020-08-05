# io_thread.py
import asyncio
import logging

import s_broker


async def start_io():
    await s_broker.start_broker()
    logging.info('io_thread stopped')
    
def main():
    logging.info('io_thread starting')
    asyncio.run(start_io())
