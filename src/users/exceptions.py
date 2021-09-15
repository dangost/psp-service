from werkzeug.exceptions import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, user_login_or_id: str = ""):
        self.code = 404
        self.description = f"User {user_login_or_id} not found"


class IncorrectPasswordException(HTTPException):
    def __init__(self):
        self.code = 403
        self.description = "Incorrect password"


class LoginAlreadyExists(HTTPException):
    def __init__(self, login: str):
        self.code = 403
        self.description = f"Login {login} already exists"


class EmailAlreadyExists(HTTPException):
    def __init__(self, email: str):
        self.code = 403
        self.description = f"Email {email} already exists"
