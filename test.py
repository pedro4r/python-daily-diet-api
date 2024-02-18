import pytest
import requests
from faker import Faker

# CRUD
BASE_URL = 'http://127.0.0.1:5000'
faker = Faker()

def test_create_user():
    user = {
        "email": faker.email(),
        "password": "newpassword"
    }
    response = requests.post(f"{BASE_URL}/user", json=user)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json

def test_login():
    # Primeiro, crie um usuário
    user = {
        "email": faker.email(),
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/user", json=user)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json

    # Agora, tente fazer login com as credenciais do usuário
    login_data = {
        "email": user["email"],
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert response_json["message"] == "User authenticated!"
    assert response.status_code == 200

def test_read_user():
    user = {
        "email": faker.email(),
        "password": "testpassword"
    }


    response = requests.post(f"{BASE_URL}/user", json=user)
    created_user_response_json = response.json()
        
    login_data = {
        "email": user["email"],
        "password": "testpassword"
    }

    with requests.Session() as s:
        response = s.post(f"{BASE_URL}/login", json=login_data)

        response = s.get(f"{BASE_URL}/user/{created_user_response_json['id']}")
        assert response.status_code == 200
        response_json = response.json()
        assert "email" in response_json
