# How to Run the Gmail RAG Assistant

This guide provides detailed instructions on how to set up and run the Gmail RAG Assistant, including both local development and deployment options.

## Prerequisites

Before running the application, ensure you have:

1. Python 3.8 or higher installed
2. An OpenAI API key
3. A Google account with Gmail
4. A Google Cloud project with the Gmail API enabled

## Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gmail-rag-assistant.git
cd gmail-rag-assistant
```

### 2. Set Up a Virtual Environment (optional but recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Set Up Google Cloud Project

#### a. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "New Project" in the top right corner
3. Enter a project name (e.g., "Gmail RAG Assistant")
4. Click "Create"

#### b. Enable the Gmail API
1. In your new project, navigate to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on it and then click "Enable"

#### c. Configure OAuth Consent Screen
1. Go to "APIs & Services" > "OAuth consent screen"
2. Select "External" user type (unless you have a Google Workspace account)
3. Fill out the required information:
   - App name: "Gmail RAG Assistant"
   - User support email: Your email address
   - Developer contact information: Your email address
4. Click "Save and Continue"
5. Add scopes:
   - Add `https://www.googleapis.com/auth/gmail.readonly`
   - Add `https://www.googleapis.com/auth/gmail.metadata`
6. Click "Save and Continue"
7. Add your email address as a test user
8. Click "Save and Continue" then "Back to Dashboard"

#### d. Create OAuth Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Select "Desktop application" or "Web application"
4. If you select "Web application", add `urn:ietf:wg:oauth:2.0:oob` as an authorized redirect URI
5. Give it a name (e.g., "Gmail RAG Assistant")
6. Click "Create"
7. Download the JSON file

#### e. Rename and Place the Credentials File
1. Rename the downloaded file to `credentials.json`
2. Place it in the project root directory

### 6. Run the Application

```bash
streamlit run app.py
```

### 7. Access the Application

The application will be available at [http://localhost:8501](http://localhost:8501) by default.

## Running on Replit

### 1. Create a New Repl

1. Go to [Replit](https://replit.com/)
2. Click "Create Repl"
3. Select "Python" as the template
4. Give your Repl a name (e.g., "gmail-rag-assistant")
5. Click "Create Repl"

### 2. Set Up Files

You can either:
- Upload all project files to Replit through the Files panel
- Or use the Replit Git integration to clone your repository

### 3. Set Up Environment Variables

1. In your Repl, click on the padlock icon (Secrets) in the left sidebar
2. Add your OpenAI API key:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

### 4. Install Dependencies

Replit will automatically install dependencies from your `pyproject.toml` or `requirements.txt` file.

If needed, you can manually install packages:
```bash
pip install streamlit openai faiss-cpu google-api-python-client google-auth-oauthlib beautifulsoup4 python-dotenv
```

### 5. Configure Streamlit for Replit

Create a `.streamlit/config.toml` file with:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

### 6. Set Up the Run Command

In the `.replit` file, set the run command to:
```
run = "streamlit run app.py --server.port 5000"
```

### 7. Run the Application

Click the "Run" button in Replit.

### 8. Upload Google Credentials

When the application is running:
1. Prepare your Google Cloud project as described in the local setup
2. Download the credentials JSON file
3. Upload it through the application's interface
4. Follow the authentication process

## Running in Demo Mode

If you don't want to connect to your real Gmail account, you can use the demo mode:

1. Run the application as described above
2. Check the "Use demo mode with sample data" checkbox in the sidebar
3. Click "Connect with Sample Data"
4. Start asking questions about the sample emails

## Troubleshooting

### Authentication Issues

- **"Invalid Client" Error**: Make sure your credentials.json file is valid and correctly formatted.
- **"Access Denied" Error**: Ensure you've completed the OAuth consent screen setup and added yourself as a test user.
- **Redirect URI Mismatch**: Make sure the redirect URI in your OAuth credentials matches what the application is using.

### Application Issues

- **"OpenAI API key not found"**: Verify that your OPENAI_API_KEY environment variable is set correctly.
- **No emails are indexed**: Check that your Gmail account has emails and that the authentication was successful.
- **High latency**: Reduce the number of emails being indexed or queried to improve performance.

## Advanced Configuration

### Customizing Email Limit

You can change the number of emails indexed by modifying the `limit` parameter in the `index_emails` method call in `app.py`.

### Using a Different OpenAI Model

If you want to use a different OpenAI model, modify the `model` parameter in the `create` method call in the `query` method of the `RAGEngine` class in `rag_engine.py`.