import os
import sys
from dotenv import load_dotenv
from PIL import Image
from utils.log_utils import log_config
from utils.rabbitmq_utils import establish_connection, close_connection, declare_queue
from utils.variables import get_env_variable
from utils.exceptions import RabbitMQException, FileException, ThumbnailException
from utils.validation import parse_json


def callback(ch, method, properties, body):
    try:
        image_task = parse_json(body, log)

        # Ensure the directory for storing thumbnails exists
        ensure_directory_exists(image_task['thumbnail_path'])

        # Simulate image processing
        generate_thumbnail(image_task['image_path'], image_task['thumbnail_path'])

        log.info(f" [x] Processed image: {image_task}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        log.error(f"An error occurred while processing the image: {e}")
        # Handle the exception appropriately, such as logging the error or re-raising it


def generate_thumbnail(input_path, output_path):
    try:
        # Example image processing function using Pillow
        with Image.open(input_path) as img:
            thumbnail = img.resize((100, 100))
            thumbnail.save(output_path)
    except FileNotFoundError as file_error:
        error_message = f"File operation error occurred: {file_error}"
        log.error(error_message)
        raise ThumbnailException(error_message)
    except PermissionError as permission_error:
        error_message = f"Permission denied: {permission_error}"
        log.error(error_message)
        raise ThumbnailException(error_message)
    except IOError as io_error:
        error_message = f"An I/O error occurred while reading from {input_path} or writing to {output_path}: {io_error}."
        log.error(error_message)
        raise ThumbnailException(error_message)
    except ValueError:
        error_message = f"The input image file {input_path} is not a valid image file."
        log.error(error_message)
        raise ThumbnailException(error_message)
    except OSError as os_error:
        error_message = f"An operating system error occurred: {os_error}"
        log.error(error_message)
        raise ThumbnailException(error_message)
    except Image.DecompressionBombError:
        error_message = "The image is too large to be processed."
        log.error(error_message)
        raise ThumbnailException(error_message)
    except Image.DecompressionBombWarning:
        error_message = "The image is potentially too large and might cause a DecompressionBombError."
        log.error(error_message)
        raise ThumbnailException(error_message)


def ensure_directory_exists(path):
    try:
        # Ensure the directory for storing thumbnails exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except FileNotFoundError as file_error:
        error_message = f"File operation error occurred: {file_error}"
        log.error(error_message)
        raise FileException(error_message)
    except PermissionError as permission_error:
        error_message = f"Permission denied: {permission_error}"
        log.error(error_message)
        raise FileException(error_message)
    except OSError as os_error:
        error_message = f"An operating system error occurred: {os_error}"
        log.error(error_message)
        raise FileException(error_message)


def start_consuming_from_queue(channel, queue_name):

    try:
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        log.info(' [*] Waiting for messages. To exit, press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        log.info('Interrupted by user')
    except Exception as e:
        log.error(f"An error occurred while consuming messages: {e}")
    finally:
        # Ensure the channel is closed properly
        if channel.is_open:
            channel.close()
            log.info('Channel closed')


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    log = log_config("work_queue")

    log.info("Starting producer...")
    try:
        log.info("Obtaining environment variables...")
        host_name = get_env_variable('HOST_NAME', log, str)
        queue_name = get_env_variable('QUEUE_NAME', log, str)
        channel = establish_connection(host_name, log)
        declare_queue(channel, queue_name, log)
    except KeyError as key_error:
        log.error(key_error)
        sys.exit(1)
    except ValueError as value_error:
        log.error(value_error)
        sys.exit(1)
    except FileException as file_error:
        log.error(file_error)
        close_connection(channel, log)
        sys.exit(1)
    except ThumbnailException as thumbnail_exception:
        log.error(thumbnail_exception)
        close_connection(channel, log)
        sys.exit(1)
    except RabbitMQException as rabbitmq_exception:
        log.error(rabbitmq_exception)
        close_connection(channel, log)
        sys.exit(1)

    # Call the start_consuming function to start consuming messages
    start_consuming_from_queue(channel, queue_name)