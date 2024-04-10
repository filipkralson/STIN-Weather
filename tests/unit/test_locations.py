def test_new_location(new_location, app):
    with app.app_context():
        assert new_location.location == 'Praha'


