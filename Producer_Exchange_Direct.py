from rabbit_mq import Rabbit, fib

rabbit = Rabbit(address='localhost', port=5672,
                exchange_type='direct', body=str(fib(40)),
                exchange_name='Direct_Exchange', routing_key='D_Exchange')
rabbit.connection()
rabbit.create_queue(exclusive=True)
rabbit.producer()
rabbit.close_connection()
