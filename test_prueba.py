import pytest
import files

@pytest.fixture
def client(request):
    client = files.app.test_client()
    return client

def test_get_files(client):
	result = client.get('/v1.0/files',follow_redirects=True)
	assert "prueba1" in result.data
	assert "prueba2" in result.data
	assert "prueba3" in result.data
