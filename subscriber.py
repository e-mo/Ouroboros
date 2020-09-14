import m_server
import queue

class Subscriber:

    def __init__(self, session):
        self.session = session.name
        self.m_type = None
        self.subscribed = False
        self.queue = queue.Queue()

    def subscribe(self, m_type):
        if not self.subscribed:
            self.m_type = m_type
            self.subscribed = True
            m_server.subscribe(self)
        else:
            logging.warning('\'%s\' already subscribed to "%s"'
                % (id(self), self.session))

    def send(self, msg):
        self.queue.put(msg)

    def recv(self):
        pass

    def unsubscribe(self):
        if self.subscribed:
            m_server.unsubscribe(self)
            self.subscribed = False
            self.m_type = None
        else:
            logging.warning('\'%s\' not subscribed' % id(self))
