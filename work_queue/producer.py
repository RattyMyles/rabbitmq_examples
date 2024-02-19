import os
import sys
from dotenv import load_dotenv
from utils.log_utils import log_config
from utils.rabbitmq_utils import establish_connection, close_connection, declare_queue, publish_message
from utils.variables import get_env_variable
from utils.exceptions import FileException, RabbitMQException


def get_image_files(image_folder):
    log.info("Processing images...")
    try:
        all_files = os.listdir(image_folder)
        log.info("Filtering files that are .jpg or .jpeg in the folder")
        jpeg_files = [file for file in all_files if file.lower().endswith(('.jpg', '.jpeg'))]
        log.debug(f"Listing images to be processed {jpeg_files}")
        log.info(f"Found {len(jpeg_files)} images to be processed")
        return jpeg_files
    except FileNotFoundError as file_error:
        error_message = f"File operation error occurred: {file_error}"
        log.error(error_message)
        raise FileException(error_message)
    except PermissionError as permission_error:
        error_message = f"Permission denied: {permission_error}"
        log.error(error_message)
        raise FileException(error_message)


def generate_image_tasks(image_folder, thumbnail_folder, image_files):
    image_tasks = []
    try:
        log.info("Processing tasks...")

        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            thumbnail_path = os.path.join(thumbnail_folder, f"{os.path.splitext(image_file)[0]}_thumbnail.jpg")

            image_task = {
                'image_path': image_path,
                'thumbnail_path': thumbnail_path
            }
            image_tasks.append(image_task)
            log.debug(f"Listing image processing tasks: {image_tasks}")
            log.info(f"Generated {len(image_tasks)} image processing tasks.")
    except FileNotFoundError as file_error:
        error_message = f"An error occurred while generating image tasks: {file_error}"
        log.error(error_message)
        raise FileException(error_message)
    return image_tasks


if __name__ == "__main__":
    load_dotenv()
    log = log_config("work_queue")

    log.info("Starting producer...")
    try:
        log.info("Obtaining environment variables...")
        host_name = get_env_variable('HOST_NAME', log, str)
        image_path = get_env_variable('IMAGE_PATH', log, str)
        thumbnail_path = get_env_variable('THUMBNAIL_PATH', log, str)
        queue_name = get_env_variable('QUEUE_NAME', log, str)

        channel = establish_connection(host_name, log)
        files_to_process = get_image_files(image_path)
        tasks_to_publish = generate_image_tasks(image_path, thumbnail_path, files_to_process)
        log.info("Declaring queue...")
        declare_queue(channel, queue_name, log)
        # List comprehension to publish messages for each image task
        [publish_message(channel, queue_name, image_task, log) for image_task in tasks_to_publish]
    except KeyError as key_error:
        log.error(key_error)
        sys.exit(1)  # Exit with status 1 indicating failure
    except ValueError as value_error:
        log.error(value_error)
        sys.exit(1)  # Exit with status 1 indicating failure
    except RabbitMQException as rabbitmq_exception:
        log.error(rabbitmq_exception)
        sys.exit(1)  # Exit with status 1 indicating failure
    except FileException as file_error:
        log.error(file_error)
        close_connection(channel, log)
        sys.exit(1)  # Exit with status 1 indicating failure
    except FileException as file_error:
        log.error(file_error)
        close_connection(channel, log)
        sys.exit(1)  # Exit with status 1 indicating failure

    close_connection(channel, log)
