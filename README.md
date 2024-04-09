# Project Title

## Overview
This project is a Flask application integrated with Elasticsearch and OpenAI for storing and searching documents based on keyword and similarity. It utilizes OpenAI's text embedding model to generate embeddings for the documents and Elasticsearch for efficient search operations.

## Features
 - Store Document: Allows storing a document in Elasticsearch along with its text and corresponding embeddings.

 - Search by Keyword: Performs a keyword-based search in Elasticsearch and returns documents containing exact words from the query. Additionally, it provides a more human response utilizing OpenAI assistant.

 - Search by Similarity: Utilizes OpenAI embeddings paired with Elasticsearch's cosine similarity to retrieve the top K most similar documents.

 - Retrieve All Documents: Retrieves all document IDs stored in Elasticsearch.

 - Retrieve Single Documents: Retrieves a particular document based on ID stored in Elasticsearch.

## Additional Description
- Keyword Search: The keyword search functionality looks for exact words in the documents and returns the documents that contain these words. Additionally, it provides a more human response utilizing OpenAI assistant for better user interaction.

- Similarity Search: The similarity search utilizes OpenAI embeddings along with Elasticsearch's cosine similarity to retrieve the top K most similar documents based on the provided query text.

## Requirements:
- OpenAI API Account. Create an accounton the [OPENAI Signup Page](https://platform.openai.com/signup)

- Start Elasticsearch.
  - Install Docker if not previously installed on Machine.
  To install Docker on your system, please visit the [Docker installation page](https://docs.docker.com/get-docker/).

  - Install and start Docker Desktop. Go to Preferences > Resources > Advanced and set Memory to at least 4GB. 
  - Start an Elasticsearch container:
    ```bash
    docker network create elastic
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.1
    docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.13.1
      ```
  - When you start Elasticsearch for the first time, the generated elastic user password and Kibana enrollment token are output to the terminal. 
  - You might need to scroll back a bit in the terminal to view the password and enrollment token.
Copy the generated password and enrollment token and save them in a secure location. These values are shown only when you start Elasticsearch for the first time.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/your_repository.git
   ```

2. Navigate to the project directory:
   ```bash
   cd your_repository
   ```

3. Create an Anaconda environment
   ```bash
   conda create -n myenv python=3.10
   source activate myenv
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Edit `constants.py` and fill in all required fields to run the application.

## Usage
1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Use the following code to send a POST request to store a document:
   ```python
   import requests

   data = {'text': 'Your text here to upload'}
   response = requests.post('http://localhost:5000/', data=data)
   print(response.json())
   ```

3. Additionally, you can use the following code to test different GET methods:
   - Search documents by keyword:
     ```python
     response = requests.get('http://localhost:5000/search_keyword?q=your_query_here')
     print(response.json())
     ```

   - Search documents by similarity:
     ```python
     response = requests.get('http://localhost:5000/search_similarity?q=your_query_here')
     print(response.json())
     ```
     
   - To retrieve a document by its ID, use the following code snippet:

     ```python
     # Replace `document_id_here` with the actual document ID you want to retrieve
     document_id = 'document_id_here'
     response = requests.get(f'http://localhost:5000/document/{document_id}')
     print(response.json())
     ```

   - Retrieve all document IDs:
     ```python
     response = requests.get('http://localhost:5000/documents')
     print(response.json())
     ```

## Testing

By including these tests, we can ensure the reliability, security, and performance of the Flask application.

### Unit Tests:
- These tests focus on individual components or functions to ensure they behave as expected. Some tests are included in `test_app.py` but it could be expanded, For example, you can write unit tests for the `get_embedding` function to check if it returns the correct embeddings for different input texts.
To run unit tests, run the following:
   ```bash
    pytest test_app.py
   ```
### Integration Tests:
- Integration tests verify that different parts of the application work together correctly. For instance, we can write tests to check if the Flask routes (`store_document`, `search_documents_by_keyword`, `search_documents_by_similarity`, `get_all_documents`) interact properly with Elasticsearch and OpenAI API.

### Security Tests: 
- Perform security tests to identify vulnerabilities such as injection attacks (e.g., SQL injection, NoSQL injection), cross-site scripting (XSS), or insecure API endpoints. Ensure that sensitive information (like API keys) is handled securely and not exposed in responses.

### Performance Tests: 
- Evaluate the performance of the application, especially for critical endpoints like search functionalities (`search_documents_by_keyword`, `search_documents_by_similarity`). 
- Measure response times under different loads and optimize where necessary to ensure scalability and responsiveness.
- Test the relevancy of the results. Is the LLM response helpful, or should the context be altered in `constants.py` for a more helpful answer?

