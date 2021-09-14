from werkzeug.exceptions import Unauthorized


class UnauthorizedException(Unauthorized):
    def __init__(self):
        self.code = 401
        self.description = "Unauthorized"
