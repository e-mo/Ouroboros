# q_manager.py
import queue
import logging

ASYNC_TIMEOUT = 0.02
KILL = 'KILL'

def create_queue(key):
    __instance.create_queue(key)

def put(key, item):
    __instance.put(key, item)

def get(key):
    return __instance.get(key)

def put_all(item):
    __instance.put_all(item)

class QueueManager:
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.__instance.queue_register = {}
        return cls.__instance

    def create_queue(self, key):
        self.queue_register[key] = queue.Queue()

    def put(self, key, item):
        self.queue_register[key].put(item)

    def get(self, key):
        msg = self.queue_register[key].get()
        return msg

    def put_all(self, item):
        for q in self.queue_register.values():
            q.put(item)

__instance = QueueManager()
