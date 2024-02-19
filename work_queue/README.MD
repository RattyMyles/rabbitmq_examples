## How to run it?
### Run RabbitMQ
First we need to start RabbitMQ and we will using the docker container.
```
docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```
This command pulls the RabbitMQ image from Docker Hub, runs it in the background with the name "some-rabbit," exposes ports 15672 for the management interface and 5672 for the AMQP protocol.

### Install the dependencies
you will need to install the packages in the requirements.txt file in order for the python scripts to run.
```
pip install -r requirements.txt
```

### Run the producer
The producer will send tasks to the work queue. The producer will send data about the raw images to be processed and the target
directory for the processed images.
```
python3 producer.py
```

### Run the consumer
The consumer will obtain tasks from the work queue. The consumer will obtain the source images and target directory.
The source images will be processed to change the resolution to 100x100 and save them to the thumbnail folder.
You can have multiple consumers("workers") continuously pulling from the work queue.
You can open up multiple terminals to create multiple consumers.
```
python3 consumer.py
```