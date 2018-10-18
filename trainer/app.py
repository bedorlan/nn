import os
import zmq
import threading
import logging

logging.basicConfig(level=logging.INFO)

context = zmq.Context()


class Subscriber(threading.Thread):
    def run(self):
        logging.info('starting')
        socket = context.socket(zmq.SUB)
        socket.connect('tcp://ctrl:3002')
        socket.subscribe('')

        while True:
            logging.info('waiting for message')
            msg = socket.recv_string()
            logging.info('new message=' + msg)


subscriber = Subscriber()
subscriber.start()
subscriber.join()
