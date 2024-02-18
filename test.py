import time
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
    user = {
        "email": faker.email(),
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/user", json=user)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json

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

def test_update_user():
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

        data = {"password": "newpassword"}

        response = s.put(f"{BASE_URL}/user/{created_user_response_json['id']}", json=data)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        assert "id" in response_json

def test_delete_user():
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

        response = s.delete(f"{BASE_URL}/user/{created_user_response_json['id']}")
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

def test_logout_user():
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
        response = s.get(f"{BASE_URL}/logout")
        assert response.status_code == 200

def test_create_meal():
    user = {
        "email": faker.email(),
        "password": "testpassword"
    }

    response = requests.post(f"{BASE_URL}/user", json=user)
        
    login_data = {
        "email": user["email"],
        "password": "testpassword"
    }

    with requests.Session() as s:
        response = s.post(f"{BASE_URL}/login", json=login_data)

        meal = {
            "name": faker.sentence(),
            "description": faker.text(),
            "inside_diet": faker.boolean()
        }

        response = s.post(f"{BASE_URL}/meal", json=meal)

        time.sleep(1)

        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        assert "id" in response_json

def test_read_meal():
    user = {
        "email": faker.email(),
        "password": "testpassword"
    }

    response = requests.post(f"{BASE_URL}/user", json=user)
        
    login_data = {
        "email": user["email"],
        "password": "testpassword"
    }

    with requests.Session() as s:
        response = s.post(f"{BASE_URL}/login", json=login_data)

        data = {
            "name": faker.sentence(),
            "description": faker.text(),
            "inside_diet": faker.boolean()
        }

        response = s.post(f"{BASE_URL}/meal", json=data)
        response_json = response.json()
        meal_id = response_json["id"]

        time.sleep(1)

        response = s.get(f"{BASE_URL}/meal/{meal_id}")
        assert response.status_code == 200
        response_json = response.json()
        response_meal = response_json["meal"]

        response_meal_id = response_meal["id"]
        assert response_meal_id == meal_id

        name = response_meal["name"]
        assert name == data["name"]

        description = response_meal["description"]
        assert description == data["description"]

        inside_diet = response_meal["inside_diet"]
        assert inside_diet == data["inside_diet"]

def test_fetch_meals():
    user = {
        "email": faker.email(),
        "password": "testpassword"
    }

    response = requests.post(f"{BASE_URL}/user", json=user)
        
    login_data = {
        "email": user["email"],
        "password": "testpassword"
    }

    with requests.Session() as s:
        response = s.post(f"{BASE_URL}/login", json=login_data)

        meal1 = {
            "name": faker.sentence(),
            "description": faker.text(),
            "inside_diet": faker.boolean()
        }

        meal2 = {
            "name": faker.sentence(),
            "description": faker.text(),
            "inside_diet": faker.boolean()
        }

        response = s.post(f"{BASE_URL}/meal", json=meal1)
        response = s.post(f"{BASE_URL}/meal", json=meal2)

        time.sleep(2)

        response = s.get(f"{BASE_URL}/meals")
        assert response.status_code == 200
        response_json = response.json()
        assert "meals" in response_json
        assert len(response_json["meals"]) > 0

def test_update_meal():
    user = {
        "email": faker.email(),
        "password": "testpassword"
    }

    response = requests.post(f"{BASE_URL}/user", json=user)
        
    login_data = {
        "email": user["email"],
        "password": "testpassword"
    }

    with requests.Session() as s:
        response = s.post(f"{BASE_URL}/login", json=login_data)

        data = {
            "name": faker.sentence(),
            "description": faker.text(),
            "inside_diet": faker.boolean()
        }

        response = s.post(f"{BASE_URL}/meal", json=data)
        response_json = response.json()
        meal_id = response_json["id"]

        time.sleep(1)

        meal = {
            "name": 'new meal',
            "description": 'new description',
            "inside_diet": True
        }

        response = s.put(f"{BASE_URL}/meal/{meal_id}", json=meal)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        reponse_meal_id = response_json["id"]
        assert reponse_meal_id == meal_id

def test_delete_meal():
    user = {
        "email": faker.email(),
        "password": "testpassword"
    }

    response = requests.post(f"{BASE_URL}/user", json=user)
        
    login_data = {
        "email": user["email"],
        "password": "testpassword"
    }

    with requests.Session() as s:
        response = s.post(f"{BASE_URL}/login", json=login_data)

        data = {
            "name": faker.sentence(),
            "description": faker.text(),
            "inside_diet": faker.boolean()
        }

        response = s.post(f"{BASE_URL}/meal", json=data)
        response_json = response.json()
        meal_id = response_json["id"]

        time.sleep(1)

        response = s.delete(f"{BASE_URL}/meal/{meal_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json