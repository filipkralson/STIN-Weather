from unittest.mock import patch, MagicMock
from project.object.users import User
from project.utils.cookies import get_current_user


def test_create_user(new_user):
    assert new_user.name == 'testUser'
    assert new_user.checkPasswd('Password')


def test_create_location(new_location):
    assert new_location.location == 'Praha'
    assert new_location.user.name == 'testUser'


def test_get_user_from_cookie(init_database):
    with patch('project.object.users.User') as mock_user:
        mock_user.query.filter_by.return_value.first.return_value.name = 'testUser'
        mock_read_cookie = MagicMock(return_value={'username': 'testUser'})

        with patch('project.utils.cookies.readCookie', mock_read_cookie):
            user = get_current_user()
            assert user is not None
            assert user.name == 'testUser'


def test_get_nonexistent_user(init_database):
    user = User.query.filter_by(name='nonexistent').first()
    assert user is None


def test_sign_up_success(test_client, init_database):
    data = {
        'user': 'testUser2',
        'password': 'password',
        'card': '9876543210987654'
    }
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200


def test_sign_up_existing_user(test_client, init_database):
    data = {
        'user': 'testUser',
        'password': 'password',
        'card': '9876543210987654'
    }
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200


def test_sign_in_success(test_client, init_database):
    data = {
        'user': 'testUser',
        'password': 'password'
    }
    response = test_client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200


def test_sign_in_invalid_credentials(test_client, init_database):
    data = {
        'user': 'testUser',
        'password': 'wrong_password'
    }
    response = test_client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200


def test_logout(test_client, init_database):
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
