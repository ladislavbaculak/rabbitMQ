import pika
from pika.spec import BasicProperties
from rabbit_mq import fib

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = conn.channel()
channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, prop, body):
    n = int(body)
    print(" [.] fib(%s)" % n)
    response = fib(n)
    channel.basic_publish(exchange='',
                          routing_key=prop.reply_to,
                          properties=pika.BasicProperties(correlation_id=prop.correlation_id),
                          body=str(response))
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
print(" [x] Awaiting RPC requests")
channel.start_consuming()
channel.close()
