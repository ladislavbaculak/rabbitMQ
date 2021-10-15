BASIC INFO:
-Rabbit MQ gotta be install on machine/server for example via Docker.
-Message Broker. Rabbit Mq act as EXCHANGE, producer emits messages and exchange sends them to the appropriate queue and consumers recieve them.
-Work as 'Post Office' you put message in mailbox and post office deliver the msg to your recipient.
-Producing: sending a message. Program that send a message is PRODUCER. Producer can only send messages to the exchange.
-Consuming: recieving a message. Program that mostly wait for recieving a message is CONSUMER.
-Queue: Place where we store the messages. It's large msg buffer. Producer send message which end up in queue and is then readed by CONSUMER. 
When we leave empty queue name RabbitMQ auto set queue, if we want to delete queue after closing the connection (exclusive=True). 
Routing_key must equal the name of the queue.
-Exchange: On one side he's recieving a messages from producer on other end it pushes them to queues. 
If message should be appended to many queues or should it get discarded. All is define by exchange type.
    Exchange types: - Direct (messages goes to the queues whose binding key mathces the routing key of the message.)
                    - Topic (topic exchange cant have arbitrary routing key - it must be list of words delimited by dots. 
                    For example: 'stock.usd.nyse.' Binding key must be the same form as routing key. Special case for binding_key is: 
                    * - can be substitute for exactly one word
                    # - can be substitute for zero or more words.
                    Word must match the pattern either is disregarded. 
                    Example: Queue1 only take binding key with *.orange.*
                             Queue2 only take binding key with *.*.rabbit and lazy.#
                             We send messages with binding key quick.orange.rabbit will go both queues, 
                             quick.orange.male.rabbit will be lost because its not match the pattern despite having 
                             the appropriate words but lazy.orange.male.rabbit will go to the Queue2.)
                    - Headers
                    - Fanout (broadcasts all messages it recieves to all queues it knows.)
-Acknowledged and durability of messages. When queue is stuck and consumer is not recieving a messages or 
connection is dropped messages are deliver to other consumers. Nothing is lost!
Message properties:
    -Delivery Mode if its value = 2 message is persistent if value is any other message is transient.
    -Content Type describe encoding. If we use JSON encoding it is good practice to set this property to application/json.
    -Reply To used to name a callback queue.
    -Correlation ID correlatying RPC responeses with request.

-Once you declare a queue as non durable you cant change it to durable. You need to declare new durable queue with different name.
-To make sure the consumer is not overflow we can use basic.qos (quality of service) protocol(prefetch_count=1). 
This method make sure consumer get only one message at time and exchange wait for response from the consumer.
-RabbitMQ have a Publish/Subscribe pattern.
-Binding: we need to tell exchange to send messages to our queue, this relationship between queue and exchange is called binding. 
We need to define binding key. Its possible to bind to multiple queues with the same binding key. 
-When using the Topic exchange you can't use basic_ack in basic_consume. 


REMOTE PROCEDURE CALL:
-RPC: Remote Procedure Call is blocking. Consider using async pipeline. Doing RPC over RabbitMQ - Client send a 
request message and server replies with a response message. 
To recieve a response client needs to send a callback queue address with the request.
    -Client start up, it creates an anonymous exclusive callback queue.
    -For RPC request, client sends a message with two properties: reply_to(which is set to the callback queue) and correlation_id(set to unique value for every request)
    -Request is send to the rpc_queue
    -RPC server is waiting for request on that queue, 
    when request appears does the job and sends a message with the result back to the client, 
    using the queue from to replay to field.
    -Client waits for data on the callback queue. When message appears it checks the correlation id. 
    If it matches the value from request it returns the response to the appliaction.
    SERVER SIDE:
        -Establish connection and declare rpc_queue
        -Set up callback on_request for basic_consume. It's executed when the request is received. It does the work and sends the response back.
        -If we want to run more than one server process. To spread the load equally over multiple servers we need to set prefetch_count setting.
    ClIENT SIDE:
        -Establish connection and declare exclusive callback_queue for replies. 
        -Subscribe to the callback_queue and we can recieve RPC responses. 
        -On_response callback that is executed on every response is checking if the correlation_id is the one we looking for. 
        If it's the id we looking for we saves response and break consuming loop. 
        -We define call method that does the actual RPC request.
        -In call method we generate a unique correlation_id and save it - on_response callback will use this ID to catch appropriate response.
        -In call method we publish the request message, with reply_to and correlation_id properties.
        -And we wait until proper response arrive and return the response back to the user.


EXAMPLE SCHEME:
(PRODUCER #1)------>|
                    |                  (Binding)
(PRODUCER #2)------>|----->(Exchange)|----------->(QUEUE)---->(CONSUMER #1)
                    |                |----------->(QUEUE)---->(CONSUMER #2)
(PRODUCER #3)------>|


DOCUMENTATION:
-https://www.rabbitmq.com/
-https://www.rabbitmq.com/tutorials/tutorial-one-python.html
-https://github.com/rabbitmq/rabbitmq-tutorials
