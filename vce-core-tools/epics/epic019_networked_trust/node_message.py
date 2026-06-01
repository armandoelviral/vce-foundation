import time


class NodeMessage:

    def create(self, sender, message_type, payload):

        return {
            "sender": sender,
            "type": message_type,
            "payload": payload,
            "timestamp": int(time.time())
        }


    def validate(self, message):

        required = [
            "sender",
            "type",
            "payload",
            "timestamp"
        ]

        for field in required:
            if field not in message:
                return False

        if not isinstance(message["sender"], str):
            return False

        if not isinstance(message["type"], str):
            return False

        if not isinstance(message["timestamp"], int):
            return False

        return True
