class Sensor:
    def __init__(self,  title: str, context: str, code:str, id: int = 0):
        self.id = id
        self.title = title
        self.context = context
        self.code = code