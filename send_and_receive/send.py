#!/usr/bin/env python
import pika


def send_message(queue_name, message):
    # Establish a connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    # Create a channel
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=queue_name)

    # Publish the message to the specified queue
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message
    )

    # Print a confirmation message
    print(f" [x] Sent '{message}' to '{queue_name}'")

    # Close the connection
    connection.close()


def main():
    # Define the queue name and message
    queue_name = 'hello'
    message = 'Hello World!'

    # Call the function to send the message
    send_message(queue_name, message)


if __name__ == "__main__":
    # Execute the main function when the script is run
    main()