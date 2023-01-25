from flaskr import create_app


def test_config():
    """Test create_app without passing test config."""
    assert not create_app('TestingConfig').testing
    assert create_app('TestingConfig').testing


def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
