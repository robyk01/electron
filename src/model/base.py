import uuid

class Component:
    def __init__(self, name):
        self.uuid = uuid.uuid4()
        self.name = name
