from rabbit_mq import Rabbit, fib

rabbit = Rabbit(address='localhost', port=5672,
                exchange_type='fanout', body=str(fib(15)),
                exchange_name='Fanout_Exchange')
rabbit.connection()
rabbit.create_queue(exclusive=True)
rabbit.producer()
rabbit.close_connection()
