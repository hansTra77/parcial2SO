import pytest
import files

@pytest.fixture
def client(request):
    client = files.app.test_client()
    return client

def get_users(client):
	return client.get('/v1.0/files',follow_redirects=True)

def test_get_users(client):
	result = get_users(client)
	assert b'files.list_files()' in result.data
