def test_create_user(test_app):
    response = test_app.post("/user/register", json={
        "email": "marvin@gmail.com",
        "password": "123456",
        "username": "Marvin",
    })
    if response.status_code == 400:
        assert response.json()['message'] == 'Email already exists'
    else:
        assert response.status_code == 201

def test_login_user(test_app):
    response = test_app.post("/user/login", json={
        "email": "marvin@gmail.com",
        "password": "123456",
    })

    assert response.status_code == 200

def test_login_user_invalid_credentials(test_app):
    response = test_app.post("/user/login", json={
        "email": "marvin@gmail.com",
        "password": "123123123"})
    assert response.status_code == 401


