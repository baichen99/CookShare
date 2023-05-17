import pytest

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

@pytest.fixture(scope="module")
def test_dish_kitchen(test_app, auth_headers):
    response = test_app.post("/kitchen/", json={
        "name": "好运来厨房",
        "description": "本厨房可以提供川菜的指导",
        "address": "上海市",
        "facilities": ["wifi", "停车场"],
    }, headers=auth_headers)
    if response.status_code == 400:
        # already exists
        kitchen = test_app.get("/kitchen/", params={
            "name": "好运来厨房"
            }, headers=auth_headers).json()['kitchens'][0]
        return kitchen
    return response.json()

@pytest.fixture(scope="module")
def test_dish(test_app, auth_headers, test_dish_kitchen):
    response = test_app.post("/dish/", json={
        "name": "宫保鸡丁",
        "description": "宫保鸡丁是一道传统的川菜",
        "price": 20,
        "kitchen_id": test_dish_kitchen['id'],
    }, headers=auth_headers)
    if response.status_code == 400:
        # already exists
        dish = test_app.get("/dish/", params={
            "name": "宫保鸡丁"
            }, headers=auth_headers).json()['dishes'][0]
        return dish
    else:
        return response.json()

def test_create_order(test_app, auth_headers, test_dish):
    response = test_app.post("/order/", json={
        "dishes_id": [test_dish['id']],
        "status": "created",
        "kitchen_id": test_dish['kitchen_id'],
    }, headers=auth_headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json()['dishes_id'] == [test_dish['id']]

