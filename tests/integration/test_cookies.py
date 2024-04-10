from flask import Response
from project.utils.cookies import createCookie, deleteCookie


def test_create_secure_cookie(app):
    with app.test_request_context():
        username = "test_user"
        response = createCookie(username)

        assert isinstance(response, Response)
        assert 'user_info' in response.headers['Set-Cookie']
        assert 'HttpOnly' in response.headers['Set-Cookie']
        assert 'SameSite=Strict' in response.headers['Set-Cookie']
        assert 'Secure' not in response.headers['Set-Cookie']
        assert response.status_code == 302
        assert response.location == "/"


def test_delete_secure_cookie_with_valid_data(app):
    with app.test_request_context():
        response = deleteCookie()

        assert response is not None
        assert "Set-Cookie" in response.headers
        assert "user_info=; Expires=Thu, 01 Jan 1970 00:00:00 GMT" in response.headers["Set-Cookie"]
        assert response.status_code == 302
        assert response.location == "/"