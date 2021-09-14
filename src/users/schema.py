from marshmallow import Schema, fields, post_load

from src.users.models import User, UserLoginDetails, UserRegistrationDetails


class UserSchema(Schema):
    id = fields.String(data_key="id", required=True)
    login = fields.String(data_key="login", required=True)
    email = fields.String(data_key="email", required=True)
    create_time = fields.DateTime(data_key="createTime", format="iso", required=True)

    @post_load
    def make(self, data, **kwargs):
        return User(**data)


class UserLoginDetailsSchema(Schema):
    login = fields.String(data_key="login", required=True)
    password = fields.String(data_key="password", required=True)

    @post_load
    def make(self, data, **kwargs):
        return UserLoginDetails(**data)


class UserRegistrationSchema(Schema):
    login = fields.String(data_key="login", required=True)
    email = fields.String(data_key="email", required=True)
    password = fields.String(data_key="password", required=True)

    @post_load
    def make(self, data, **kwargs):
        return UserRegistrationDetails(**data)


user_schema = UserSchema()
user_login_schema = UserLoginDetailsSchema()
user_registration_schema = UserRegistrationSchema()
