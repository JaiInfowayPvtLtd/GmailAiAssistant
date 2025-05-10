# Gmail RAG Assistant - Technical Architecture

## System Overview

The Gmail RAG Assistant is a Retrieval-Augmented Generation (RAG) system that connects to a user's Gmail inbox and enables natural language queries. The application is built using a modular architecture with the following key components:

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│                 │       │                 │       │                 │
│  Streamlit UI   │◄─────►│ RAG Engine      │◄─────►│  Gmail Service  │
│                 │       │                 │       │                 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
        ▲                         ▲                         ▲
        │                         │                         │
        ▼                         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│                 │       │                 │       │                 │
│     OpenAI      │       │  FAISS Vector   │       │  Google OAuth   │
│     API         │       │     Store       │       │     & API       │
│                 │       │                 │       │                 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

## Core Components

### 1. Streamlit UI (`app.py`)

The front-end interface built with Streamlit provides:
- User authentication flow with Google OAuth
- Email content display and search functionality
- Chat interface for natural language queries
- Demo mode for testing without real Gmail credentials
- Session state management for persistent user experience

### 2. Gmail Service (`gmail_service.py`)

This component handles all interactions with the Gmail API:
- OAuth authentication and token management
- Retrieval of emails, threads, and metadata
- Email content parsing and cleaning
- Search functionality for specific email queries
- Error handling and retry logic for API requests

### 3. RAG Engine (`rag_engine.py`)

The core intelligence layer that implements the Retrieval-Augmented Generation pattern:
- Email vectorization using OpenAI embeddings
- Vector storage and search using FAISS
- Integration with OpenAI's GPT models for response generation
- Context preparation and prompt engineering
- Query parsing and relevance determination

### 4. Utilities (`utils.py`)

Supporting functions and helpers:
- File handling for credentials and uploads
- Date formatting and parsing
- Natural language query parameter extraction
- Sample data generation for demo mode

## Data Flow

1. **Authentication Flow**:
   ```
   User → Upload Credentials → Google OAuth → Token Storage → Gmail API Access
   ```

2. **Email Indexing Flow**:
   ```
   Gmail API → Fetch Emails → Parse Content → Generate Embeddings → Store in FAISS
   ```

3. **Query Flow**:
   ```
   User Query → Embedding Generation → FAISS Similarity Search → Retrieve Relevant Emails → Context Building → GPT Response Generation → User Interface
   ```

## Technical Implementation Details

### Gmail Authentication

The application uses OAuth 2.0 to securely authenticate with Gmail:
- Credentials are loaded from a `credentials.json` file provided by the user
- The OAuth flow is handled through Google's authentication libraries
- Tokens are cached locally in `token.json` for persistence
- The application requests read-only scopes to ensure minimal access requirements

### Email Vectorization

Emails are converted to vector representations for semantic search:
- Each email is processed to extract key information (sender, date, subject, body)
- The text is cleaned and formatted into a standardized representation
- OpenAI's text-embedding-3-small model generates 1536-dimensional vectors
- These vectors are normalized and stored in a FAISS index for efficient retrieval

### FAISS Vector Store

Facebook AI Similarity Search (FAISS) is used for vector storage and retrieval:
- Uses an L2 index for efficient similarity search
- Vectors are stored alongside their corresponding email metadata
- The index is saved to disk for persistence between sessions
- Supports fast k-nearest neighbor search for finding relevant emails

### RAG Implementation

The Retrieval-Augmented Generation approach combines:
1. **Retrieval**: Finding the most relevant emails based on vector similarity
2. **Augmentation**: Extracting and formatting relevant content as context
3. **Generation**: Using GPT-4o to generate responses based on the retrieved context

### Response Generation

The OpenAI GPT model is prompted with:
- A system message defining the assistant's role and capabilities
- The user's natural language query
- Retrieved email context formatted for optimal understanding
- Parameters set for appropriate temperature and response length

## Error Handling and Resilience

The application implements comprehensive error handling:
- Gmail API connection and rate limit errors
- OAuth authentication failures
- Email parsing and content extraction errors
- Vector embedding generation failures
- Response generation timeouts or errors

## Performance Considerations

- Email indexing is limited to the most recent emails (default: 100) to manage API usage
- Embeddings are generated once and cached to minimize OpenAI API calls
- Vector similarity search is optimized for fast retrieval
- OAuth tokens are refreshed automatically to maintain consistent access

## Security Considerations

- All credentials and tokens are stored locally
- Only necessary Gmail scopes are requested (read-only access)
- No email content is stored in third-party services
- Vector embeddings do not contain the original email text
- Users can revoke access at any time through their Google account

## Extension Points

The modular architecture allows for several extension possibilities:
- Support for additional email providers beyond Gmail
- Integration with other vector stores beyond FAISS
- Support for additional language models beyond OpenAI
- Enhanced query capabilities with advanced NLP techniques
- Email analytics and visualization components