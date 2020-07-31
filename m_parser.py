# m_parser.py
import asyncio

import m_server

async def parse_message(session, msg):
    sorted_msg = sort_message(msg)
    await m_server.distribute(session, sorted_msg)
    await m_server.subscribe('poop', 'moyalinka', 'raw')

def sort_message(msg):
    return {'raw': msg, 'skoot': 'map stuff'}

if __name__ == '__main__':
    asyncio.run(parse_message('moyalinka', 'meow time baby'))
