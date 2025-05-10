# Gmail RAG Assistant

## Overview

Gmail RAG Assistant is an AI-powered tool that combines the Gmail API with OpenAI's language models through Retrieval-Augmented Generation (RAG) to help you interact with your email inbox using natural language. Ask questions about your emails, search for specific content, get summaries, and more - all through a simple chat interface.

## Features

- 🔒 **Secure Gmail Authentication**: Connect securely to your Gmail account using OAuth2
- 🔍 **Semantic Search**: Find relevant emails using advanced vector similarity search
- 💬 **Natural Language Queries**: Ask about your emails in plain English
- 🧠 **AI-Powered Responses**: Get intelligent answers from OpenAI's GPT models
- 📊 **Email Insights**: Extract patterns and information from your email history
- 🛠️ **Demo Mode**: Test the functionality with sample emails before connecting to your real account

## Getting Started

### Prerequisites

- A Google account with Gmail
- An OpenAI API key
- Google Cloud project with Gmail API enabled
- OAuth 2.0 credentials for the Google Cloud project

### Installation and Setup

1. **Clone this repository**:
   ```
   git clone <repository-url>
   cd gmail-rag-assistant
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Set up your environment variables**:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Set up Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Gmail API for your project
   - Configure the OAuth consent screen
   - Create OAuth credentials (Desktop or Web application)
   - Download the credentials as `credentials.json`

5. **Run the application**:
   ```
   streamlit run app.py
   ```

6. **Connect to Gmail**:
   - Upload your `credentials.json` file in the app
   - Follow the OAuth authentication flow
   - Start querying your emails!

## Usage

### Demo Mode

If you want to try the application without connecting to your real Gmail account, you can use the demo mode:

1. Check the "Use demo mode with sample data" checkbox
2. Click "Connect with Sample Data"
3. Start asking questions about the sample emails

### Querying Your Emails

Once connected to Gmail, you can ask questions like:

- "What emails did I receive from Amazon last week?"
- "Summarize the last 5 unread messages."
- "Do I have any emails from my boss this month?"
- "Find emails with attachments from the last 10 days."
- "What are the most recent emails in my Primary folder?"

### Refreshing Email Index

To ensure your email index is up to date:

1. Click the "Refresh Email Index" button in the sidebar
2. The application will fetch and index your most recent emails

## Technical Architecture

The application is built using:

- **Streamlit**: For the web interface
- **Google API Client**: For Gmail API integration
- **OpenAI API**: For embeddings and language model capabilities
- **FAISS**: For efficient vector similarity search
- **BeautifulSoup4**: For HTML content parsing

For more details about the architecture, see the [ARCHITECTURE.md](ARCHITECTURE.md) file.

## Security and Privacy

- Your emails are processed locally and are not stored permanently
- OAuth tokens are stored locally for persistent authentication
- No email content is sent to third parties other than OpenAI (for generating embeddings and responses)
- You can revoke the application's access to your Gmail account at any time through [Google Security Settings](https://myaccount.google.com/security)

## Troubleshooting

### Authentication Issues

- Ensure your `credentials.json` file is valid and has the correct scopes
- If you encounter "Invalid Grant" errors, try the authentication process again

### No Emails Found

- Check if your Gmail account has accessible emails
- Try refreshing the email index
- Verify that the authentication was successful

### API Rate Limits

- The application may be limited by Google API or OpenAI API rate limits
- If you encounter rate limit errors, try again after some time

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the AI models
- Google for the Gmail API
- The Streamlit team for the wonderful web framework