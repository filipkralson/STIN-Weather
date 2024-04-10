def test_main_post():
    pass


def test_main_get(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_main_weather():
    pass


def test_main_add_to_favourite():
    pass
