## Introduction

In this section, we'll craft two concise Python programs – a producer responsible for sending a singular message and a consumer designed to receive and display messages. This exercise serves as a fundamental introduction, often referred to as the "Hello World" of messaging.

## Overview

Refer to the diagram below for a visual representation of our setup. The producer is denoted by "P," and the consumer is represented by "C." The intermediary box is a queue, functioning as a message buffer managed by RabbitMQ on behalf of the consumer.

[P] -----> Queue -----> [C]

## prerquites
- Docker


## How to run it?
### Run RabbitMQ
First we need to start RabbitMQ and we will using the docker container.
```
docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```
This command pulls the RabbitMQ image from Docker Hub, runs it in the background with the name "some-rabbit," exposes ports 15672 for the management interface and 5672 for the AMQP protocol.
### Send a message to the queue
Execute the following command to send a message.
```python3 send.py```

### receive a message
Run the following command to receive a message.
```python3 receive.py```

### list queues
For insights into message sending and consumption within the Docker container, list the queues using one of the following commands.
```
docker exec -it some-rabbit bash
rabbitmqctl list_queues
exit
```
OR
```
docker exec -it some-rabbit rabbitmqctl list_queues
```
