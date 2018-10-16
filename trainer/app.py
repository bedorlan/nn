import pika

params = pika.ConnectionParameters(host='broker', connection_attempts=6, retry_delay=10)
conn = pika.BlockingConnection(params)
