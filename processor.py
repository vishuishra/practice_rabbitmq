# processor.py
import pika

def process_message(message: str):
    # Process the message, in this case, appending "World" to it
    processed_message = message + " World"
    return processed_message

def on_message(channel, method_frame, header_frame, body):
    message = body.decode()
    processed_message = process_message(message)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="output_queue")
    channel.basic_publish(exchange='',
                          routing_key="output_queue",
                          body=processed_message)
    connection.close()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="input_queue")
    channel.basic_consume(queue="input_queue", on_message_callback=on_message, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
