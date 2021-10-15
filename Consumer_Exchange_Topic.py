from rabbit_mq import Rabbit

rabbit = Rabbit(address='localhost', port=5672,
                exchange_type='topic', binding_key='#',
                exchange_name='Topic_Exchange')
rabbit.connection()
rabbit.exchange_declaring()
rabbit.create_queue(exclusive=True)
rabbit.binding()
rabbit.consumer()
