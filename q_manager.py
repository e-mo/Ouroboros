# q_manager.py
import queue
import logging

ASYNC_TIMEOUT = 0.02
KILL = 'kill'

def put(key, item):
    __instance.put(key, item)

def get(key):
    return __instance.get(key)

def kill(session):
    __instance.put(session, KILL)

def kill_all():
    __instance.put_all(KILL)

class QueueManager:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.__instance.queue_register = {}
        return cls.__instance

    def __create_queue(self, key):
        self.queue_register[key] = queue.Queue()

    def put(self, key, item):
        if key not in self.queue_register:
            self.__create_queue(key)
        self.queue_register[key].put(item)
            
    def get(self, key):
        if key not in self.queue_register:
            self.__create_queue(key)
        msg = self.queue_register[key].get()
        return msg

    def put_all(self, item):
        for q in self.queue_register.values():
            q.put(item)

__instance = QueueManager()
