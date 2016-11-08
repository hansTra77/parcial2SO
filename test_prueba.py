import pytest
import files, json, files_recently

@pytest.fixture
def client(request):
    client = files.app.test_client()
    return client

def test_get_files(client):
	result = client.get('/v1.0/files',follow_redirects=True)
	assert "prueba1" in result.data
	assert "prueba2" in result.data
	
def test_post_create(client):
        nuevo = {'filename': 'casaaaa', 'content': 'esta es una casa'}
	result = client.post('/v1.0/files', data = json.dumps(nuevo), content_type='application/json')
	assert result.status == '200 OK'
	assert get_file_content("casaaaa") == "esta es una casa"

def test_delete_file(client):
	client.delete('/v1.0/files', follow_redirects=True)
	result = client.get('/v1.0/files',follow_redirects=True)
	assert "prueba1" not in result.data
	
def test_get_recents(client):
	result = client.get('/v1.0/files/recently_created',follow_redirects=True)
	assert "pruebaa" in result.data
