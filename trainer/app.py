import os
import zmq
import threading
import logging
import json
import trainer

logging.basicConfig(level=logging.INFO)

logging.info('starting')
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://ctrl:3002')
socket.subscribe('')

trainjob = None
while True:
    logging.info('waiting for message')
    msg = socket.recv_string()
    logging.info('new message=' + msg)
    state = json.loads(msg)

    if trainjob is None:
        trainjob = trainer.Trainer()
        trainjob.init(state['train'])
        trainjob.start()
    else:
        trainjob.stop()
        trainjob = None
