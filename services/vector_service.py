import pinecone
from sentence_transformers import SentenceTransformer
from config import Config
import logging
import numpy as np

class VectorService:
    def __init__(self):
        self.config = Config()
        self.model = None
        self.index = None
        
        # Initialize local embeddings model
        if self.config.USE_LOCAL_EMBEDDINGS:
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                logging.info("Local embeddings model loaded")
            except Exception as e:
                logging.error(f"Failed to load local embeddings: {e}")
        
        # Initialize Pinecone
        if self.config.PINECONE_API_KEY:
            try:
                pinecone.init(
                    api_key=self.config.PINECONE_API_KEY,
                    environment=self.config.PINECONE_ENVIRONMENT
                )
                
                # Create index if it doesn't exist
                if self.config.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                    pinecone.create_index(
                        name=self.config.PINECONE_INDEX_NAME,
                        dimension=384,  # all-MiniLM-L6-v2 dimension
                        metric='cosine'
                    )
                
                self.index = pinecone.Index(self.config.PINECONE_INDEX_NAME)
                logging.info("Pinecone initialized")
            except Exception as e:
                logging.error(f"Pinecone initialization failed: {e}")
    
    def embed_text(self, text):
        """Generate embeddings for text"""
        if self.model:
            return self.model.encode([text])[0].tolist()
        else:
            # Fallback: simple hash-based pseudo-embedding
            return [hash(text) % 1000 / 1000.0] * 384
    
    def store_knowledge(self, text, metadata=None):
        """Store text in vector database"""
        if not self.index:
            return False
        
        try:
            embedding = self.embed_text(text)
            vector_id = f"doc_{hash(text)}"
            
            self.index.upsert([{
                'id': vector_id,
                'values': embedding,
                'metadata': metadata or {'text': text}
            }])
            return True
        except Exception as e:
            logging.error(f"Failed to store knowledge: {e}")
            return False
    
    def search_knowledge(self, query, top_k=3):
        """Search for relevant knowledge"""
        if not self.index:
            return []
        
        try:
            query_embedding = self.embed_text(query)
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            return [match.metadata.get('text', '') for match in results.matches]
        except Exception as e:
            logging.error(f"Knowledge search failed: {e}")
            return []