def test_signup(test_client):
    response = test_client.post('/register')
    assert response.status_code == 200


def test_logout(test_client):
    response = test_client.get('/logout')
    assert response.status_code == 302


def test_login(test_client):
    response = test_client.post('/login')
    assert response.status_code == 200
