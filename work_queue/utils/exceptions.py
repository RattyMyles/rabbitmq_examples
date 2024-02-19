class FileException(Exception):
    def __init__(self, message="File exception"):
        self.message = message
        super().__init__(self.message)


class ThumbnailException(Exception):
    def __init__(self, message="Thumbnail exception"):
        self.message = message
        super().__init__(self.message)


class RabbitMQException(Exception):
    def __init__(self, message="RabbitMQ exception"):
        self.message = message
        super().__init__(self.message)


class JSONException(Exception):
    def __init__(self, message="JSON exception"):
        self.message = message
        super().__init__(self.message)
