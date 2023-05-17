import pytest

@pytest.fixture(scope="module")
def dish_auth_headers(test_app):
    # create test_user
    response = test_app.post("/user/register", json={
        "email": "test_dish_user@gmail.com",
        "password": "123456",
        "username": "test_dish_user"
    })
    response = test_app.post("/user/login", json={
        "email": "test_dish_user@gmail.com",
        "password": "123456",
    })
    token = response.json()['access_token']
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def test_dish_kitchen(test_app, dish_auth_headers):
    response = test_app.post("/kitchen/", json={
        "name": "好运来厨房",
        "description": "本厨房可以提供川菜的指导",
        "address": "上海市",
        "facilities": ["wifi", "停车场"],
    }, headers=dish_auth_headers)
    if response.status_code == 400:
        # already exists
        kitchen = test_app.get("/kitchen/", params={
            "name": "好运来厨房"
            }, headers=dish_auth_headers).json()['kitchens'][0]
        return kitchen
    return response.json()

def test_create_dish(test_app, dish_auth_headers, test_dish_kitchen):
    response = test_app.post("/dish/", json={
        "name": "宫保鸡丁",
        "description": "宫保鸡丁是一道传统的川菜",
        "price": 20,
        "kitchen_id": test_dish_kitchen['id'],
    }, headers=dish_auth_headers)
    assert response.status_code == 201

def test_update_dish(test_app, dish_auth_headers, test_dish_kitchen):
    dish = test_app.get("/dish/", params={
        "name": "宫保鸡丁",
        "kitchen_id": test_dish_kitchen['id'],
    }, headers=dish_auth_headers).json()['dishes'][0]
    
    response = test_app.put(f"/dish/{dish['id']}", json={
        "price": 30,
    }, headers=dish_auth_headers)
    assert response.status_code == 204
    # 验证修改
    response = test_app.get(f"/dish/{dish['id']}", headers=dish_auth_headers)
    assert response.status_code == 200
    assert response.json()['price'] == 30
    
def test_get_dishes(test_app, dish_auth_headers, test_dish_kitchen):
    response = test_app.get("/dish/", params={
        "name": "宫保鸡丁",
        "kitchen_id": test_dish_kitchen['id'],
    }, headers=dish_auth_headers)
    
    assert response.status_code == 200
    assert response.json()['dishes'][0]['name'] == "宫保鸡丁"
    
def test_delete_dish(test_app, dish_auth_headers, test_dish_kitchen):
    dish = test_app.get("/dish/", params={
        "name": "宫保鸡丁",
        "kitchen_id": test_dish_kitchen['id'],
    }, headers=dish_auth_headers).json()['dishes'][0]
    
    response = test_app.delete(f"/dish/{str(dish['id'])}", headers=dish_auth_headers)

    assert response.status_code == 204
    # 验证删除
    response = test_app.get(f"/dish/{str(dish['id'])}", headers=dish_auth_headers)
    assert response.status_code == 404
