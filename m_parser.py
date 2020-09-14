# m_parser.py
import asyncio
import logging

import m_server

async def parse_message(session, msg):
    logging.info('"%s" parsing msg \'%s\'' % (session, msg))
    parsed_msg = __parse(msg)
    await m_server.distribute(session, parsed_msg)

def __parse(msg):
    parsed_msg = {'raw': msg}
    lines = msg.decode().split('\r\n')
    return parsed_msg

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(parse_message('moyalinka', 'meow time baby'))
