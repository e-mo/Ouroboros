import select
import queue
from acctsock import AcctSock

class SockHandler:

    def __init__(self):
        self.socks = {}
        self.next_sid = 0
        self.message_queues = {'recv': {}, 'send': {}}

    def new_sock(self, uname = 'n/a', pwd = 'n/a'):
        new_sock = AcctSock(self.next_sid)

        self.socks[new_sock.sid] = new_sock
        self.message_queues['recv'][new_sock.sid] = queue.Queue()
        self.message_queues['send'][new_sock.sid] = queue.Queue()

        # Send inital connect message to login with provided info
        # 'n/a' for both will trigger login prompt from server
        connect_msg = '/\\/Connect: ' + uname + '!!' + pwd
        self.send(new_sock.sid, connect_msg)
        self.next_sid += 1

    '''
    Polls all open sockets for their status.
    If waiting to be read, read to buffer
    If ready to be written to, write from send buffer
    '''
    def poll(self):
        readable, writable, exception = select.select(
                self.socks.values(), self.socks.values(), self.socks.values())

        for sock in readable:
            recv_queue = self.message_queues['recv'][sock.sid]
            sock.recv(recv_queue)
            
        for sock in writable:
            send_queue = self.message_queues['send'][sock.sid]
            if not send_queue.empty():
                sock.send(send_queue)

        for sock in exception:
            pass

    def send(self, sid, msg):
        # Server accepts messages in utf-8 terminated with a newline char
        msg = msg.encode() + b'\n'
        send_queue = self.message_queues['send'][sid]
        send_queue.put(msg)

    def recv(self, sid):
        recv_queue = self.message_queues['recv'][sid]
        return recv_queue
