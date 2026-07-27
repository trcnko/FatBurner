from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_create_product():
    payload = {
        'name': 'Тестовый Апельсин',
        'calories': 43,
        'proteins': 0.9,
        'fats': 0.2,
        'carbs': 8.1
    }
    response = client.post('/products', json=payload)
    assert response.status_code == 200
    assert response.json()['name'] == 'Тестовый Апельсин'
    assert response.json()['calories'] == 43
    assert response.json()['proteins'] == 0.9
    assert response.json()['fats'] == 0.2
    assert response.json()['carbs'] == 8.1

def test_get_products():
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.parametrize('user_name, target_cal', (
    ('TestMasha', 1500),
    ('TestPasha', 2500),
    ('TestVanya', 3000)
))
def test_create_user(user_name, target_cal):
    payload = {
        'name': user_name,
        'daily_target': target_cal,
        'password': 'password123'
    }
    response = client.post('/users', json=payload)
    assert response.status_code in [200, 400]

def test_create_user_short_password():
    payload = {
        'name': 'shortNikita',
        'daily_target': 2500,
        'password': '123'
    }
    response = client.post('/users', json=payload)
    assert response.status_code == 422

def test_create_duplicate_name_user():
    payload = {
        'name': 'DuplicateUser',
        'daily_target': 2000,
        'password': 'password123'
    }
    client.post('/users', json=payload)

    response = client.post('/users', json=payload)
    assert response.status_code == 400
    assert 'уже занят' in response.json()['detail']

def test_login_success():
    payload_reg = {
        'name': 'LoginTestUser',
        'daily_target': 2000,
        'password': 'password123'
    }
    client.post('/users', json=payload_reg)

    payload_login = {
        'name': 'LoginTestUser',
        'password': 'password123'
    }
    response = client.post('/login', json=payload_login)
    assert response.status_code == 200
    assert response.json()['user_name'] == 'LoginTestUser'

def test_login_wrong_password():
    payload_reg = {
        'name': 'WrongPasswordUser',
        'daily_target': 2000,
        'password': 'password123'
    }
    client.post('/users', json=payload_reg)

    payload_login = {
        'name': 'WrongPasswordUser',
        'password': 'wrongpassword'
    }
    response = client.post('/login', json=payload_login)
    assert response.status_code == 401

def test_create_meal():
    products = client.get("/products").json()
    if not products:
        client.post('/products', json={
            'name': 'Тестовый продукт',
            'calories': 100,
            'proteins': 10,
            'fats': 5,
            'carbs': 15
        })
        products = client.get('/products').json()
    payload = {
        'user_name': 'TestMasha',
        'product_id': products[0]['product_id'],
        'grams': 150.0,
        'date': '2026-07-21'
    }
    response = client.post('/meals', json=payload)
    assert response.status_code == 200

def test_create_meal_nonexistent_user():
    payload = {
        'user_name': 'GhostUser',
        'product_id': 1,
        'grams': 100,
        'date': '2026-07-21'
    }
    response = client.post('/meals', json=payload)
    assert response.status_code == 404

def test_get_user_stats():
    response = client.get('/users/TestMasha/stats', params={'date_query': '2026-07-21'})
    assert response.status_code == 200
    assert response.json()['user_name'] == 'TestMasha'
    assert 'daily_target' in response.json()
    assert 'total_eaten' in response.json()
    assert 'meals_history' in response.json()

def test_delete_meal_success():
    products = client.get("/products").json()
    if not products:
        client.post('/products', json={
            'name': 'Тестовый продукт для удаления',
            'calories': 100,
            'proteins': 10,
            'fats': 5,
            'carbs': 15
        })
        products = client.get('/products').json()

    payload = {
        'user_name': 'TestMasha',
        'product_id': products[0]['product_id'],
        'grams': 100.0,
        'date': '2026-07-22'
    }
    create_response = client.post('/meals', json=payload)
    meal_id = create_response.json()['meal_id']

    delete_response = client.delete(f'/meals/{meal_id}')
    assert delete_response.status_code == 200