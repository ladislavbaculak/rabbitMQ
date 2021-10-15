from rabbit_mq import Rabbit, fib

rabbit = Rabbit(address='localhost', port=5672,
                exchange_type='topic', body=str(fib(10)),
                exchange_name='Topic_Exchange', routing_key='#')
rabbit.connection()
rabbit.create_queue()
rabbit.producer()
rabbit.close_connection()
