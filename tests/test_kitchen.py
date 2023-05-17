import pytest


@pytest.fixture(scope="module")
def admin_headers(test_app):
    # create test_admin
    response = test_app.post("/admin/login", json={
        "email": "admin@example.com",
        "password": "password",
    })
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def auth_headers(test_app):
    # create test_user
    test_app.post("/user/register", json={
        "email": "testuser@gmail.com",
        "password": "123456",
        "username": "test_user"
    })
    response = test_app.post("/user/login", json={
        "email": "testuser@gmail.com",
        "password": "123456",
    })
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}

def test_create_kitchen(test_app, auth_headers):
    response = test_app.post("/kitchen/", json={
        "name": "Marvin's Kitchen",
        "description": "You can eat anything here",
        "address": "Shanghai",
        "facilities": ["wifi", "parking"],
    }, headers=auth_headers)
    if response.status_code == 400:
        assert response.json()['message'] in ['You can only create 3 kitchens', 'Kitchen name already exists']
    else:
        assert response.status_code == 201

def test_get_kitchens(test_app, auth_headers):
    response = test_app.get("/kitchen/", headers=auth_headers)
    assert response.status_code == 200

def test_get_kitchens_by_owner_id(test_app, auth_headers, admin_headers):
    # get user id
    response = test_app.get("/user/", headers=admin_headers, params={
        "username": "test_user"
    })
    user = response.json()['users'][0]
    response = test_app.get("/kitchen/", params={
        "owner_id": user['id']
    }, headers=auth_headers)
    assert response.status_code == 200

def test_update_kitchen(test_app, auth_headers):
    kitchen = test_app.get("/kitchen/", params={
        "name": "Marvin's Kitchen"
    }, headers=auth_headers).json()['kitchens'][0]
    
    response = test_app.put(f"/kitchen/{str(kitchen['id'])}", json={
        "facilities": ["wifi", "parking", "air-conditioning"],
    }, headers=auth_headers)
    assert response.status_code == 204


def test_delete_kitchen(test_app, auth_headers):
    kitchen = test_app.get("/kitchen/", params={
        "name": "Marvin's Kitchen"
    }, headers=auth_headers).json()['kitchens'][0]
    
    response = test_app.delete(f"/kitchen/{str(kitchen['id'])}", headers=auth_headers)
    assert response.status_code == 204