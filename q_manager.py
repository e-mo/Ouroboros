# q_manager.py
import queue
import logging

ASYNC_TIMEOUT = 0.02
KILL = 'kill'

def put(key, msg):
    __instance.put(key, msg)

def get(key):
    return __instance.get(key)

def get_nowait(key):
    return __instance.get(key, wait=False)

def kill(session):
    for queue in __instance.queue_register:
        if queue.startswith(session):
            __instance.put(queue, KILL)

def kill_all():
    __instance.put_all(KILL)

def exists(key):
    return __instance.exists(key)

class QueueManager:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.__instance.queue_register = {}
        return cls.__instance

    def __create_queue(self, key):
        logging.info('creating queue "%s"' % key)
        self.queue_register[key] = queue.Queue()

    def put(self, key, msg):
        #logging.info('putting \'%s\' --> "%s"' % (msg, key))
        logging.info('putting --> "%s"' % key)
        if key not in self.queue_register:
            self.__create_queue(key)
        self.queue_register[key].put(msg)
            
    def get(self, key, wait=True):
        logging.info('getting <-- "%s"' % key)
        if key not in self.queue_register:
            self.__create_queue(key)
        if wait:
            msg = self.queue_register[key].get()
        else:
            try:
                msg = self.queue_register[key].get_nowait()
            except queue.Empty:
                msg = None
        return msg

    def put_all(self, msg):
        for key in self.queue_register:
            self.put(key, msg)

    def exists(self, key):
        return key in self.queue_register

__instance = QueueManager()
