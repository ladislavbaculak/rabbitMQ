from rabbit_mq import Rabbit

rabbit = Rabbit(address='localhost', port=5672,
                exchange_type='direct',
                exchange_name='Direct_Exchange',
                binding_key='D_Exchange')
rabbit.connection()
rabbit.exchange_declaring()
rabbit.create_queue(exclusive=True)
rabbit.binding()
rabbit.consumer()
