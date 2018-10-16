import os
import pika
import logging

logging.basicConfig(level=logging.INFO)

params = pika.ConnectionParameters(host='broker', connection_attempts=6, retry_delay=10)
conn = pika.BlockingConnection(params)

ch = conn.channel()
ch.queue_declare(queue='get_models')

for method, props, body in ch.consume('get_models'):
    logging.info('new message=' + body)
    dirs = [d for d in os.listdir('./models')]
    response = str(dirs)

    if props.reply_to:
        logging.info('replying to=' + props.reply_to)
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=response)

    ch.basic_ack(delivery_tag=method.delivery_tag)
