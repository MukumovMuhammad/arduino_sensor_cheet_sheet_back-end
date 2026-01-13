class Sensor:
    def __init__(
            self,
            title: str, 
            context: str, 
            code:str,
            title_img:str, 
            scheme_img: str,
            id: int = 0
            ):
        self.id = id
        self.title = title
        self.context = context
        self.code = code
        self.title_img = title_img
        self.scheme_img = scheme_img

    def get_values(self):
        return (self.title, self.context, self.code, self.title_img, self.scheme_img)