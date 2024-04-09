import pytest
from app2_cosine import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_store_document(client):
    response = client.post('/', data={'text': 'Test document'})
    assert response.status_code == 201
    assert 'document_id' in response.json


def test_search_documents_by_keyword(client):
    response = client.get('/search_keyword?q=test')
    assert response.status_code == 200
    assert 'LLM Output' in response.json
    assert 'raw_output' in response.json


def test_search_documents_by_similarity(client):
    response = client.get('/search_similarity?q=test&k=3')
    assert response.status_code == 200
    assert 'LLM Output' in response.json
    assert 'raw_output' in response.json


def test_get_all_documents(client):
    response = client.get('/documents')
    assert response.status_code == 200
    assert 'document_ids' in response.json
    assert isinstance(response.json['document_ids'], list)
