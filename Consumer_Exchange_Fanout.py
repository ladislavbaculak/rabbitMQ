from rabbit_mq import Rabbit

rabbit = Rabbit(address='localhost', port=5672,
                exchange_type='fanout',
                exchange_name='Fanout_Exchange')
rabbit.connection()
rabbit.exchange_declaring()
rabbit.create_queue(exclusive=True)
rabbit.binding()
rabbit.consumer()
