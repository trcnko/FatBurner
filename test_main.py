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
        'daily_target': target_cal
    }
    response = client.post('/users', json=payload)
    assert response.status_code in [200, 400]

def test_create_meal():
    payload = {
        'user_name': 'TestMasha',
        'product_id': client.get("/products").json()[0]['product_id'],
        'grams': 150.0,
        'date': '2026-07-21'
    }
    response = client.post('/meals', json=payload)
    assert response.status_code == 200

def test_get_user_stats():
    response = client.get('/users/TestMasha/stats', params={'date_query': '2026-07-21'})
    assert response.status_code == 200
    assert response.json()['user_name'] == 'TestMasha'
    assert 'daily_target' in response.json()
    assert 'total_eaten' in response.json()
    assert 'meals_history' in response.json()