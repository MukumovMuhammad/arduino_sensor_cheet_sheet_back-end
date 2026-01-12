class Sensor:
    def __init__(self,  title: str, context: str, code:str,image_path:str, id: int = 0):
        self.id = id
        self.title = title
        self.context = context
        self.code = code
        self.image_path = image_path