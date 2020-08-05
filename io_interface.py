# io_interface.py

import s_broker

def start_session(uname, pwd):
    s_broker.send_msg(s_broker.START, uname, pwd)

def end_session(session):
    s_broker.send_msg(s_broker.END, session)
    
