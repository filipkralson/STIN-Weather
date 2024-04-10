def test_payment_success(test_client, new_user):
    with test_client.session_transaction() as sess:
        sess['username'] = new_user.name

    response = test_client.post('/payment')
    assert response.status_code == 302


def test_payment_user_not_logged_in(test_client):
    response = test_client.post('/payment')
    assert response.status_code == 302


def test_payment_user_not_found(test_client):
    with test_client.session_transaction() as sess:
        sess['username'] = 'nonexistent_user'

    response = test_client.post('/payment')
    assert response.status_code == 302
