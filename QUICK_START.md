# Gmail RAG Assistant - Quick Start Guide

This quick start guide will help you get up and running with the Gmail RAG Assistant in just a few minutes.

## 1. Prerequisites

- OpenAI API key
- Google account with Gmail

## 2. Running the Application

### Option 1: Run on Replit

1. Fork this Replit project
2. Add your OpenAI API key to Replit Secrets:
   - Click on the lock icon in the sidebar
   - Add `OPENAI_API_KEY` as the key and your API key as the value
3. Click the Run button
4. The application will open in the webview

### Option 2: Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gmail-rag-assistant.git
   cd gmail-rag-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Open your browser at http://localhost:8501

## 3. Using the Application

### Demo Mode (No Gmail Credentials Required)

1. Check the "Use demo mode with sample data" checkbox in the sidebar
2. Click "Connect with Sample Data"
3. Start asking questions to interact with the sample email data

### Connect to Your Gmail Account

1. Create a Google Cloud project:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Gmail API
   - Configure the OAuth consent screen
   - Create OAuth credentials (Desktop or Web application)
   - Download the JSON credentials file

2. Upload your credentials:
   - In the app sidebar, upload your credentials.json file
   - Click "Connect to Gmail"
   - Follow the authorization steps

3. Start querying your emails:
   - Use the chat interface to ask questions about your emails
   - Try example questions from the sidebar

## 4. Sample Questions to Try

- "What emails did I receive from Amazon last week?"
- "Summarize the last 5 unread messages."
- "Do I have any emails from my boss this month?"
- "Find emails with attachments from the last 10 days."
- "What are the most recent emails in my Primary folder?"

## 5. Additional Features

- **Refresh Email Index**: Click this button in the sidebar to update your email index with the latest emails
- **Logout**: Click to disconnect from your Gmail account

## Need More Help?

- Check the [HOW_TO_RUN.md](HOW_TO_RUN.md) file for detailed setup instructions
- See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details about how the application works
- Refer to [README.md](README.md) for a complete overview of features and capabilities