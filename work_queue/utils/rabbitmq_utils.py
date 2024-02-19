import pika
import json
from utils.exceptions import RabbitMQException


def establish_connection(host_name, log):
    log.info("Establishing RabbitMQ connection...")
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_name))
        channel = connection.channel()
        log.info("Established RabbitMQ connection")
        return channel
    except pika.exceptions.AMQPConnectionError as connection_error:
        error_message = f"Error establishing connection to RabbitMQ: {connection_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except pika.exceptions.ProbableAuthenticationError as auth_error:
        error_message = f"Authentication error: {auth_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except pika.exceptions.ProbableAccessDeniedError as access_denied:
        error_message = f"Access denied: {access_denied}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except pika.exceptions.ChannelClosedByBroker as channel_closed:
        error_message = f"Channel closed by broker: {channel_closed}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except pika.exceptions.ConnectionClosedByBroker as connection_closed:
        error_message = f"Connection closed by broker: {connection_closed}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except pika.exceptions.UnexpectedFrameError as frame_error:
        error_message = f"Unexpected frame error: {frame_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except pika.exceptions.AMQPChannelError as amqp_channel_error:
        error_message = f"AMQP channel error: {amqp_channel_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except pika.exceptions.AMQPError as general_amqp_error:
        error_message = f"General AMQP error: {general_amqp_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)


def close_connection(connection, log):
    """Close the RabbitMQ connection."""
    try:
        return connection.close()
    except AttributeError as attr_error:
        # Handle any attribute errors
        error_message = f"Attribute error occurred while closing RabbitMQ connection: {attr_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except ConnectionError as connection_error:
        # Handle any connection errors
        error_message = f"Connection error occurred while closing RabbitMQ connection: {connection_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)
    except pika.exceptions.AMQPError as general_amqp_error:
        # Handle other general AMQP errors
        error_message = f"AMQP error occurred while closing RabbitMQ connection: {general_amqp_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)


def declare_queue(channel, queue_name, log):
    try:
        return channel.queue_declare(queue=queue_name)
    except pika.exceptions.AMQPError as amqp_error:
        # Handle AMQP errors
        error_message = f"AMQP error occurred while declaring the queue: {amqp_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)


def publish_message(channel, queue_name, message, log):
    log.info(f"Publishing {message} to queue: {queue_name}")
    try:
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message)
        )
        log.info(f"Successfully published")
    except pika.exceptions.AMQPError as amqp_error:
        error_message = f"AMQP error occurred while publishing message: {amqp_error}"
        log.error(error_message)
        raise RabbitMQException(error_message)
