import queue
from sockhandler import SockHandler

sh = SockHandler()
sh.new_sock()

while True:
    sh.poll()
    recv_queue = sh.recv(0)
    if not recv_queue.empty():
        print(recv_queue.get().decode())
