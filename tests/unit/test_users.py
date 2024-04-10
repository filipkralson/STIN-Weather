def test_create_user(new_user):
    assert new_user.name == "testUser"
    assert new_user.password != "Password"
    assert new_user.card_number == "123456789123456"


