# OpenAI Configuration
OPENAI_API_KEY = ''  # API key to connect to OpenAI

# Elasticsearch Configuration
ELASTICSEARCH_USER = ''  # Elasticsearch username
ELASTICSEARCH_PASSWORD = ''  # Elasticsearch password
ELASTICSEARCH_PORT = 9200  # Port Elasticsearch is running on
ELASTICSEARCH_INDEX = 'documents'  # Elasticsearch index name

# OpenAI Model Configuration
OPENAI_EMBEDDINGS_MODEL = "text-embedding-3-small"  # OpenAI embedding model name
OPENAI_EMBEDDING_SIZE = 1536  # OpenAI embedding model vector size
OPENAI_LANGUAGE_MODEL = "gpt-3.5-turbo"  # OpenAI language model name

# Sample Contexts for Language Model Response
KEYWORD_SEARCH_CONTEXT = """
You are a master of clean data outputs. You will receive a list of text documents that a user has looked up by keyword.
After a friendly introduction, provide a well-organized response that is more human-readable than what is provided.
If the list is empty, inform the user accordingly. Do not output anything after providing the answer.
"""
SIMILARITY_SEARCH_CONTEXT = """
You are a master of clean data outputs. You will receive a list of text documents that a user has looked up by vector similarity search.
The data should be outputted in the same order as the list. After a friendly introduction, give a well-organized response that is more human-readable than what is provided.
If the list is empty, inform the user accordingly. Do not output anything after providing the answer.
"""

# Top K Results for Similarity Search
TOP_K_SIMILARITY = 3  # Number of top results to respond to similarity search
