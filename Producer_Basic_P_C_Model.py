from rabbit_mq import Rabbit, fib

rabbit = Rabbit('localhost', 5672, body=str(fib(15)),
                queue_name='task_queue', routing_key='task_queue')
rabbit.connection()
rabbit.create_queue(durable=True)
rabbit.producer()
rabbit.close_connection()
