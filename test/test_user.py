
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.user_schema import UserResponse

client =  TestClient(app)

def test_root():
    res = client.get('/')
    assert res.status_code == 200
    assert res.json().get('message') == 'hello world!'

def test_create_user():
    res = client.post('/users', json={'email': 'user@example.com', 'password': 'test'})
    user = UserResponse(**res.json())

    assert res.status_code == 201
    assert user.email == 'user@example.com'