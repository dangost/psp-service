import requests

from tests.integrational.conftest import get_str


def test_create_user(host):
    email_ = f"{get_str()}@gmail.com"
    login_ = f"{get_str()}"
    password_ = f"{get_str()}"
    user_payload = {
        "email": email_,
        "login": login_,
        "password": password_
    }

    response = requests.post(f"{host}/api/registration", json=user_payload)
    assert response.status_code == 200

    response = requests.post(f"{host}/api/registration", json=user_payload)
    assert response.status_code == 403
    assert response.json() == {
        "message": f"Login {login_} already exists",
        "statusCode": 403
    }

    new_user_payload = {
        "email": email_,
        "login": get_str(),
        "password": password_
    }
    response = requests.post(f"{host}/api/registration", json=new_user_payload)
    assert response.status_code == 403
    assert response.json() == {
        "message": f"Email {email_} already exists",
        "statusCode": 403
    }
