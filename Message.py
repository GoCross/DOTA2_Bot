

class Message:

    id = 0

    message = ''

    send_succeed = False

    def __init__(self, id, message, send_succeed):
        self.id = id
        self.message = message
        self.send_succeed = send_succeed
