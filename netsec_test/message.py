import json


class Message(object):

    def __init__(self, command, data=None):

        self.command = command
        self.data = data if data else {}

    def serialize(self):
        return json.dumps({
            "command": self.command,
            "data": self.data
        }) + "\n"

    @classmethod
    def deserialize(cls, msg):
        parsed = json.loads(msg.strip())
        command = parsed.get("command")
        data = parsed.get("data")
        return cls(command=command, data=data)