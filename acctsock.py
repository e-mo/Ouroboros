import socket
import queue

class AcctSock:
    HOST = 'tec.skotos.net'
    PORT = 6730

    def __init__(self, sid):
        self.sid = sid

        self.__create_sock()
        self.__connect()
        self.sock.setblocking(0)
        
    def __create_sock(self):
        try:
            self.sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print(e)

    def __connect(self):
        try:
            self.sock.connect((self.HOST, self.PORT))
        except socket.gaierror as e:
            print(e)

    def recv(self, recv_queue):
        try:
            data = self.sock.recv(1024) 
        except sock.error as e:
            print(e)
        else:
            recv_queue.put(data)

    def send(self, send_queue):
        try:
            msg = send_queue.get_nowait()
            self.sock.sendall(msg)
        except queue.Empty:
            pass
        except socket.error as e:
            print(e)
    
    # This allows us to pass an AcctSock object into select.select method
    def fileno(self):
        return self.sock.fileno()
