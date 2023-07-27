# practice_rabbitmq
Created a fast-API application that would publish a simple message on a message queue in rabbitmq.  A core python processer.py that would listen to this message and append "World" to it, and publish the message on a different topic. Now fast API application has to listen to that processed message and return the processed message to client. 
