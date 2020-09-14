import s_broker
import s_manager

class Session:

    def __init__(self, uname, pwd):
        self.name = uname
        s_broker.send_msg(s_broker.START, uname, pwd)

    def end(self):
        s_broker.send_msg(s_broker.END, self.name)
        
    def send(self, msg):
        s_manager.send(self.name, msg)
