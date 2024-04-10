from unittest.mock import patch


def test_post_no_user(test_client):
    data = {'city': 'London', 'add_to_favorites': 'Submit'}
    response = test_client.post('/', data=data)
    assert response.status_code == 302


def test_post_add_to_favorites(test_client, new_user):
    with patch('project.controller.main.get_current_user') as mock_get_current_user:
        mock_get_current_user.return_value = new_user
        data = {'city': 'London', 'add_to_favorites': 'Submit'}
        response = test_client.post('/', data=data)
        assert response.status_code == 302


def test_get_authenticated(test_client, new_user):
    with patch('project.controller.main.get_current_user') as mock_get_current_user:
        mock_get_current_user.return_value = new_user
        response = test_client.get('/')
        assert response.status_code == 200


def test_get_unauthenticated(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_weather_authenticated(test_client, new_user):
    with patch('project.utils.cookies.get_current_user') as mock_get_current_user:
        mock_get_current_user.return_value = new_user
        with patch('project.controller.main.get_favorites') as mock_get_favorites:
            mock_get_favorites.return_value = ['London']
            response = test_client.get('/weather?location=London')
            assert response.status_code == 200


def test_weather_unauthenticated(test_client):
    with patch('project.utils.cookies.get_current_user') as mock_get_current_user:
        mock_get_current_user.return_value = None
        response = test_client.get('/weather?location=London')
        assert response.status_code == 200


def test_add_to_favourite_authenticated(test_client, new_user):
    with patch('project.utils.cookies.get_current_user') as mock_get_current_user:
        mock_get_current_user.return_value = new_user
        response = test_client.get('/addToFavourite?location=London')
        assert response.status_code == 302


def test_add_to_favourite_unauthenticated(test_client):
    # Test adding to favorites when user is not authenticated
    response = test_client.get('/addToFavourite?location=London')
    assert response.status_code == 302  # Assuming it redirects to sign-in page
