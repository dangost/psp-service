import requests

from tests.integrational.conftest import get_str


def test_login_and_auth(host: str):
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

    keys = {
        "login": login_,
        "password": password_
    }
    response = requests.post(f"{host}/api/auth", json=keys)
    assert response.status_code == 200

    jwt_token = response.json()['Authorization']

    response = requests.get(f"{host}/api/me", headers={'Authorization': jwt_token})

    assert response.status_code == 200
    assert response.json()['login'] == login_
