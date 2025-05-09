import os
import json
import faiss
import numpy as np
from datetime import datetime
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGEngine:
    def __init__(self, gmail_service=None):
        """Initialize the RAG Engine with Gmail service and OpenAI integration."""
        self.gmail_service = gmail_service
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set it in the .env file.")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Initialize vector storage
        self.dimension = 1536  # OpenAI embeddings dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.emails = []
        self.index_file = "email_index.index"
        self.emails_file = "emails_data.json"
        self.is_demo_mode = gmail_service is None
        
        # Load existing index if available and not in demo mode
        if not self.is_demo_mode:
            self._load_index()
    
    def _get_embedding(self, text):
        """Generate embedding for text using OpenAI API."""
        # Limit text length to avoid token limits
        if len(text) > 8000:
            text = text[:8000]
            
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def _save_index(self):
        """Save the FAISS index and email data to disk."""
        # Save FAISS index
        faiss.write_index(self.index, self.index_file)
        
        # Save email data
        with open(self.emails_file, 'w') as f:
            json.dump(self.emails, f)
    
    def _load_index(self):
        """Load the FAISS index and email data from disk if they exist."""
        if os.path.exists(self.index_file) and os.path.exists(self.emails_file):
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.emails_file, 'r') as f:
                    self.emails = json.load(f)
                return True
            except Exception as e:
                print(f"Error loading index: {e}")
                return False
        return False
    
    def index_emails(self, limit=100, force_refresh=False):
        """Index emails for vector search."""
        if len(self.emails) > 0 and not force_refresh:
            return len(self.emails)
        
        # Don't proceed if in demo mode or if Gmail service is not available
        if self.is_demo_mode or self.gmail_service is None:
            return len(self.emails)
        
        # Clear existing index if forcing refresh
        if force_refresh:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.emails = []
        
        # Fetch recent emails
        raw_emails = self.gmail_service.get_recent_emails(count=limit)
        
        # Process and index each email
        for email in raw_emails:
            # Create document for indexing
            email_text = f"Subject: {email['subject']}\nFrom: {email['sender']}\nDate: {email['date']}\n\n{email['body_text']}"
            
            # Get embedding
            embedding = self._get_embedding(email_text)
            
            # Add to FAISS index
            embedding_array = np.array([embedding], dtype=np.float32)
            faiss.normalize_L2(embedding_array)
            self.index.add(embedding_array)
            
            # Store email data without HTML content to save space
            email_data = {
                'id': email['id'],
                'thread_id': email['thread_id'],
                'subject': email['subject'],
                'sender': email['sender'],
                'date': email['date'],
                'snippet': email['snippet'],
                'body_text': email['body_text'],
                'labels': email['labels']
            }
            self.emails.append(email_data)
        
        # Save index and data
        self._save_index()
        
        return len(self.emails)
    
    def _create_index_from_samples(self, sample_emails):
        """Create FAISS index from sample emails for demo mode."""
        # Clear any existing index
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Process and index each sample email
        for email in sample_emails:
            # Create document for indexing
            email_text = f"Subject: {email['subject']}\nFrom: {email['sender']}\nDate: {email['date']}\n\n{email['body_text']}"
            
            # Get embedding
            embedding = self._get_embedding(email_text)
            
            # Add to FAISS index
            embedding_array = np.array([embedding], dtype=np.float32)
            faiss.normalize_L2(embedding_array)
            self.index.add(embedding_array)
        
        return len(sample_emails)
    
    def _search_similar_emails(self, query, top_k=5):
        """Search for emails similar to the query."""
        query_embedding = self._get_embedding(query)
        query_embedding_normalized = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_embedding_normalized)
        
        # Search the index
        D, I = self.index.search(query_embedding_normalized, top_k)
        
        # Get the corresponding emails
        results = []
        for idx in I[0]:
            if idx < len(self.emails) and idx >= 0:
                results.append(self.emails[idx])
        
        return results
    
    def query(self, user_query):
        """Process a natural language query about emails."""
        # Check if we have indexed emails
        if len(self.emails) == 0:
            return "No emails have been indexed yet. Please refresh the email index."
        
        # Search for relevant emails
        relevant_emails = self._search_similar_emails(user_query)
        
        if not relevant_emails:
            return "I couldn't find any relevant emails for your query."
        
        # Prepare context from relevant emails
        context = "Here are the most relevant emails for your query:\n\n"
        for i, email in enumerate(relevant_emails):
            context += f"EMAIL {i+1}:\n"
            context += f"Subject: {email['subject']}\n"
            context += f"From: {email['sender']}\n"
            context += f"Date: {email['date']}\n"
            context += f"Snippet: {email['snippet']}\n"
            
            # Add truncated body if it's not too long
            body_preview = email['body_text'][:500] + "..." if len(email['body_text']) > 500 else email['body_text']
            context += f"Body: {body_preview}\n\n"
        
        # Generate response with OpenAI
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    "You are an AI assistant specializing in helping users navigate their Gmail inbox. "
                    "Answer the user's question based only on the provided email context. "
                    "If you can't answer based on the provided emails, explain why and suggest "
                    "how they might refine their query. Be concise, helpful, and direct. "
                    "Don't reference yourself as an AI or mention the context beyond answering the query."
                )},
                {"role": "user", "content": f"Here is my question about my emails:\n{user_query}\n\nContext from my emails:\n{context}"}
            ],
            temperature=0.3,
            max_tokens=800
        )
        
        return response.choices[0].message.content
