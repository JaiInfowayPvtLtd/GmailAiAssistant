import os
import pickle
import base64
import html
import re
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

class GmailService:
    def __init__(self, credentials_path):
        """Initialize the Gmail service with OAuth authentication."""
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.metadata']
        self.credentials_path = credentials_path
        self.service = self.authenticate()
        
    def authenticate(self):
        """Authenticate with Gmail API using OAuth."""
        creds = None
        token_path = 'token.json'
        
        # Load credentials from token.json if it exists
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If credentials don't exist or are invalid, refresh them
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        # Build the Gmail service
        return build('gmail', 'v1', credentials=creds)
    
    def get_user_profile(self):
        """Get the user's Gmail profile information."""
        return self.service.users().getProfile(userId='me').execute()
    
    def list_labels(self):
        """List all available Gmail labels."""
        results = self.service.users().labels().list(userId='me').execute()
        return results.get('labels', [])
    
    def list_messages(self, query='', max_results=100):
        """List messages matching the given query."""
        result = self.service.users().messages().list(
            userId='me', q=query, maxResults=max_results).execute()
        messages = result.get('messages', [])
        return messages
    
    def get_message(self, msg_id):
        """Get full message details by message ID."""
        message = self.service.users().messages().get(userId='me', id=msg_id).execute()
        return message
    
    def get_message_content(self, message):
        """Extract and decode email content from a message."""
        if 'payload' not in message:
            return {
                'id': message['id'],
                'thread_id': message['threadId'],
                'snippet': message.get('snippet', ''),
                'subject': 'No Subject',
                'sender': 'Unknown',
                'date': '',
                'body_text': '',
                'body_html': '',
                'labels': message.get('labelIds', [])
            }
        
        # Extract headers
        headers = message['payload']['headers']
        subject = ''
        sender = ''
        date = ''
        
        for header in headers:
            if header['name'].lower() == 'subject':
                subject = header['value']
            elif header['name'].lower() == 'from':
                sender = header['value']
            elif header['name'].lower() == 'date':
                date = header['value']
        
        # Extract body content
        body_text = ''
        body_html = ''
        
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    body_data = part['body']['data']
                    body_text = base64.urlsafe_b64decode(body_data).decode('utf-8')
                elif part['mimeType'] == 'text/html' and 'data' in part['body']:
                    body_data = part['body']['data']
                    body_html = base64.urlsafe_b64decode(body_data).decode('utf-8')
        elif 'body' in message['payload'] and 'data' in message['payload']['body']:
            body_data = message['payload']['body']['data']
            decoded_data = base64.urlsafe_b64decode(body_data).decode('utf-8')
            if message['payload']['mimeType'] == 'text/html':
                body_html = decoded_data
            else:
                body_text = decoded_data
        
        # If we have HTML but no plain text, extract text from HTML
        if body_html and not body_text:
            soup = BeautifulSoup(body_html, 'html.parser')
            body_text = soup.get_text(separator=' ', strip=True)
        
        # Clean up the text content
        body_text = html.unescape(body_text)
        body_text = re.sub(r'\s+', ' ', body_text).strip()
        
        return {
            'id': message['id'],
            'thread_id': message['threadId'],
            'snippet': message.get('snippet', ''),
            'subject': subject,
            'sender': sender,
            'date': date,
            'body_text': body_text,
            'body_html': body_html,
            'labels': message.get('labelIds', [])
        }
    
    def get_recent_emails(self, count=100):
        """Get the most recent emails with full content."""
        # List recent messages
        messages = self.list_messages(max_results=count)
        
        # Fetch full content for each message
        emails = []
        for msg in messages:
            full_msg = self.get_message(msg['id'])
            email_content = self.get_message_content(full_msg)
            emails.append(email_content)
        
        return emails
    
    def search_emails(self, query, count=30):
        """Search emails with a specific query and get full content."""
        # List messages matching the query
        messages = self.list_messages(query=query, max_results=count)
        
        # Fetch full content for each message
        emails = []
        for msg in messages:
            full_msg = self.get_message(msg['id'])
            email_content = self.get_message_content(full_msg)
            emails.append(email_content)
        
        return emails
