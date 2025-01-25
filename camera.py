class Camera:
    def __init__(self, ):
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 1

    def MoveCamera(self, direction: str, speed: int = 1):
        speed = speed + self.scale  # Makes moving camera faster depending on current size.
        match direction:
            case "up":
                self.camera_y += speed

            case "down":
                self.camera_y -= speed

            case "left":
                self.camera_x += speed

            case "right":
                self.camera_x -= speed

            case _:
                return False
        return True

    def ChangeScale(self, direction: str, speed: int = 1):
        speed = speed + self.scale / 10  # Makes scaling faster depending on current size.
        match direction:
            case "more":
                self.scale += speed
            # self.camera_x += self.scale
            # self.camera_y += self.scale

            case "less":
                self.scale -= speed
            # self.camera_x -= self.scale
            # self.camera_y -= self.scale

            case _:
                return False

        if self.scale < 0.1:
            self.scale = 0.1
        return True

    def Reset(self, ):
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 1
        print("Render location & Scale reset")