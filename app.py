from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import numpy as np
import uuid
from typing import Dict, Any
import openai
import constants

app = Flask(__name__)

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=constants.OPEN_AI_KEY)

# Initialize Elasticsearch client with host information
es = Elasticsearch([{'host': 'localhost', 'port': constants.ELASTICSEARCH_PORT, "scheme": "https"}],
                   verify_certs=False,
                   http_auth=(constants.ELASTICSEARCH_USER, constants.ELASTICSEARCH_PASSWORD))

# Define Elasticsearch index and document type
INDEX_NAME = constants.ELASTICSEARCH_INDEX

def create_index():
    """
    Create the Elasticsearch index if it doesn't exist.

    This function checks if the specified Elasticsearch index exists. If not,
    it creates the index with the necessary mappings for storing document embeddings.
    """
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body={
            "mappings": {
                "properties": {
                    "text_vector": {
                        "type": "dense_vector",
                        "dims": constants.OPEN_AI_EMBEDDING_SIZE  # Dimensionality of OpenAI's embeddings
                    }
                }
            }
        })

def get_embedding(text, model="text-embedding-3-small"):
    """
    Generate embeddings for the given text.

    Uses OpenAI's text embedding model to generate embeddings for the provided text.

    Args:
        text (str): The input text for which embeddings are to be generated.
        model (str, optional): The name of the OpenAI embedding model to be used.
            Defaults to "text-embedding-3-small".

    Returns:
        list: A list representing the embedding vector for the input text.
    """
    text = text.replace("\n", " ")
    return openai_client.embeddings.create(input=[text], model=model).data[0].embedding

@app.route('/', methods=['POST'])
def store_document():
    """
    Store a document in Elasticsearch.

    This endpoint allows storing a document in Elasticsearch along with its text
    and corresponding embeddings.

    Returns:
        JSON: A JSON object containing the ID of the stored document if successful,
        or an error message if text is not provided.
    """
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            document_id = str(uuid.uuid4())
            document = {'text': text}

            # Get embeddings for the document text using OpenAI's embeddings
            embedding = get_embedding(text)

            document['text_vector'] = embedding

            es.index(index=INDEX_NAME, id=document_id, body=document)
            return jsonify({'document_id': document_id}), 201
        else:
            return jsonify({'error': 'Text not provided'}), 400

@app.route('/search_keyword', methods=['GET'])
def search_documents_by_keyword() -> Dict[str, Any]:
    """
    Search documents in Elasticsearch by keyword.

    This endpoint performs a keyword-based search in Elasticsearch and returns
    a list of IDs of matching documents.

    Returns:
        JSON: A JSON object containing the LLM output and raw output of the search results.
    """
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Search query must be provided in the "q" parameter.'}), 400

    body = {
        'query': {'query_string': {'query': query}}
    }

    results = es.search(index=INDEX_NAME, body=body)
    results = [hit['_id'] for hit in results['hits']['hits']]

    completion = openai_client.chat.completions.create(
        model=constants.OPEN_AI_MODEL,
        messages=[
            {"role": "system",
             "content": constants.KEYWORD_SEARCH_CONTEXT},
            {"role": "user", "content": str(results)}
        ]
    )
    return_json = {"LLM Output": str(completion.choices[0].message),
                   "raw_output": results}
    return jsonify(return_json), 200

@app.route('/search_similarity', methods=['GET'])
def search_documents_by_similarity():
    """
    Search documents in Elasticsearch by similarity.

    This endpoint performs a similarity-based search in Elasticsearch and returns
    the top k similar documents.

    Returns:
        JSON: A JSON object containing the LLM output and raw output of the search results.
    """
    query_text = request.args.get('q')
    k = int(request.args.get('k', constants.TOP_K_SIMILARITY))  # Default value of k is 10

    if query_text:
        query_vector = get_embedding(query_text)
        query_vector = np.array(query_vector).tolist()

        search_body = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector,'text_vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
            "size": k  # Limiting the search results to top k documents
        }
        response = es.search(index=INDEX_NAME, body=search_body)

        search_results = [{"document_id": hit['_id'], "score": hit['_score']} for hit in response['hits']['hits']]

        completion = openai_client.chat.completions.create(
            model=constants.OPEN_AI_MODEL,
            messages=[
                {"role": "system",
                 "content": constants.SIMILARITY_SEARCH_CONTEXT},
                {"role": "user", "content": str(search_results)}
            ]
        )
        return_json = {"LLM Output": str(completion.choices[0].message),
                       "raw_output": search_results}

        return jsonify(return_json), 200
    else:
        return jsonify({"error": "Query text not provided"}), 400

@app.route('/documents', methods=['GET'])
def get_all_documents():
    """
    Retrieve all document IDs from Elasticsearch.

    This endpoint retrieves all document IDs stored in Elasticsearch.

    Returns:
        JSON: A JSON object containing the list of document IDs if successful,
        or an error message if an exception occurs during retrieval.
    """
    try:
        response = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}})
        document_ids = [hit['_id'] for hit in response['hits']['hits']]
        return jsonify({"document_ids": document_ids}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

<<<<<<< HEAD

@app.route('/document/<document_id>', methods=['GET'])
def get_document_by_id(document_id):
    """
    Retrieve a document from Elasticsearch by its ID.

    This endpoint retrieves a document stored in Elasticsearch based on its Document ID.

    Args:
        document_id (str): The ID of the document to retrieve.

    Returns:
        JSON: A JSON object containing the document if found,
        or an error message if the document does not exist.
    """
    try:
        document = es.get(index=INDEX_NAME, id=document_id)
        text = document["_source"]["text"]
        return jsonify({"text": text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

=======
>>>>>>> 624ea767a070f6a3e7c24098ac7109d8e4d896c2
if __name__ == '__main__':
    create_index()
    app.run(debug=True)
