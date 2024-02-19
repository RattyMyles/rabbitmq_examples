#!/usr/bin/env python
import pika
import sys
import os


def receive_messages():
    # Establish a connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    # Create a channel
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='hello')

    # Define the callback function to process received messages
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # Set up the consumer and specify the callback function
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    # Display a message indicating that the script is waiting for messages
    print(' [*] Waiting for messages. To exit, press CTRL+C')

    # Start consuming messages
    channel.start_consuming()


if __name__ == '__main__':
    try:
        # Call the main function to start receiving messages
        receive_messages()
    except KeyboardInterrupt:
        # Handle keyboard interruption
        print('Interrupted')
        try:
            # Attempt to gracefully exit the script
            sys.exit(0)
        except SystemExit:
            # If sys.exit fails, forcefully exit the script
            os._exit(0)