from rabbit_mq import Rabbit

rabbit = Rabbit('localhost', 5672,
                queue_name='task_queue')
rabbit.connection()
rabbit.create_queue(durable=True)
rabbit.consumer(auto_ack=False)
