import os
import zmq
import threading
import logging
import json
import trainer

logging.basicConfig(level=logging.INFO)

logging.info('starting')
context = zmq.Context()

requester = context.socket(zmq.REQ)
requester.connect('tcp://ctrl:3001')

subscriber = context.socket(zmq.SUB)
subscriber.connect('tcp://ctrl:3002')
subscriber.subscribe('')


def send_train_result(result):
    data = {"event": "train_result", "content": result}
    requester.send(json.dumps(data))
    requester.recv_string()


def send_predict_result(result):
    data = {"event": "predict_result", "content": result}
    requester.send(json.dumps(data))
    requester.recv_string()


trainjob = None
while True:
    msg = subscriber.recv_string()
    state = json.loads(msg)

    if trainjob is None and 'train' in state:
        trainjob = trainer.Trainer()
        trainjob.init(state['train'])
        trainjob.on_epoch_end.on_any(send_train_result)
        logging.info('start trainer msg=' + msg)
        trainjob.start()

    elif trainjob is not None and "train" not in state:
        # si el campo train esta vacio: me detengo
        logging.info('stop trainer')
        trainjob.stop()
        trainjob.join()
        trainjob = None

    elif "predict" in state and "predictResult" not in state:
        logging.info('predict msg=' + msg)
        y = state['predict']
        ynew = trainer.predict(y)
        send_predict_result(ynew)
