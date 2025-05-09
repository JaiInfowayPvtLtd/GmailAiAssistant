import os
import streamlit as st
import json
from datetime import datetime, timedelta

def save_uploaded_file(uploaded_file, save_path):
    """Save an uploaded file to the specified path."""
    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return False

def get_sample_emails():
    """Return a list of sample emails for demo mode."""
    # Create a set of sample emails for demonstration purposes
    sample_emails = [
        {
            'id': '1',
            'thread_id': '1',
            'subject': 'Welcome to our service',
            'sender': 'support@example.com',
            'date': (datetime.now() - timedelta(days=2)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Welcome to our service! We are excited to have you on board.',
            'body_text': 'Welcome to our service! We are excited to have you on board. Here are some tips to get you started...',
            'labels': ['INBOX', 'CATEGORY_UPDATES']
        },
        {
            'id': '2',
            'thread_id': '2',
            'subject': 'Your order #12345 has shipped',
            'sender': 'orders@amazon.com',
            'date': (datetime.now() - timedelta(days=5)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Your recent order #12345 has shipped and is on its way.',
            'body_text': 'Your recent order #12345 has shipped and is on its way. Expected delivery date is in 2-3 business days. Your order contains: 1x Smartphone case, 1x Screen protector.',
            'labels': ['INBOX', 'CATEGORY_UPDATES']
        },
        {
            'id': '3',
            'thread_id': '3',
            'subject': 'Meeting agenda for tomorrow',
            'sender': 'boss@company.com',
            'date': (datetime.now() - timedelta(days=1)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Here is the agenda for our team meeting tomorrow at 10 AM.',
            'body_text': 'Here is the agenda for our team meeting tomorrow at 10 AM:\n1. Project updates\n2. Budget review\n3. Upcoming deadlines\n4. Open discussion\n\nPlease come prepared with your weekly progress report.',
            'labels': ['INBOX', 'CATEGORY_PERSONAL', 'IMPORTANT']
        },
        {
            'id': '4',
            'thread_id': '4',
            'subject': 'Your subscription renewal',
            'sender': 'billing@netflix.com',
            'date': (datetime.now() - timedelta(days=3)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Your Netflix subscription will automatically renew on June 15, 2023.',
            'body_text': 'Your Netflix subscription will automatically renew on June 15, 2023. Your account will be charged $14.99 for the standard plan. If you want to make changes to your subscription, please visit your account settings.',
            'labels': ['INBOX', 'CATEGORY_PROMOTIONS']
        },
        {
            'id': '5',
            'thread_id': '5',
            'subject': 'Invitation to speak at conference',
            'sender': 'events@techconference.com',
            'date': (datetime.now() - timedelta(days=6)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'We would like to invite you to speak at our upcoming tech conference.',
            'body_text': 'We would like to invite you to speak at our upcoming tech conference on July 10-12, 2023. We believe your expertise in AI would be valuable to our audience. The session would be 45 minutes long, followed by a 15-minute Q&A. Please let us know if you are interested and available.',
            'labels': ['INBOX', 'CATEGORY_PERSONAL', 'UNREAD']
        },
        {
            'id': '6',
            'thread_id': '6',
            'subject': 'Your flight itinerary',
            'sender': 'noreply@airline.com',
            'date': (datetime.now() - timedelta(days=4)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Your upcoming flight itinerary for your trip to New York on June 20.',
            'body_text': 'Your upcoming flight itinerary for your trip to New York on June 20:\nFlight: AA123\nDeparture: Los Angeles (LAX) at 10:30 AM\nArrival: New York (JFK) at 7:15 PM\nConfirmation code: ABC123\n\nBaggage allowance: 1 checked bag, 1 carry-on\nSeat assignment: 14A (Window)',
            'labels': ['INBOX', 'CATEGORY_UPDATES', 'IMPORTANT']
        },
        {
            'id': '7',
            'thread_id': '7',
            'subject': 'Weekly team newsletter',
            'sender': 'newsletter@company.com',
            'date': (datetime.now() - timedelta(days=1)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Here is your weekly company newsletter with updates and announcements.',
            'body_text': 'Here is your weekly company newsletter with updates and announcements.\n\nAnnouncements:\n- New health benefits package starting next month\n- Office will be closed for renovation on May 15-16\n- Welcome our new team member, Jane Smith\n\nUpcoming Events:\n- Company picnic on June 3\n- Quarterly review meetings next week\n- Product launch on May 30',
            'labels': ['INBOX', 'CATEGORY_UPDATES']
        },
        {
            'id': '8',
            'thread_id': '8',
            'subject': 'Your invoice #INV-567',
            'sender': 'billing@supplier.com',
            'date': (datetime.now() - timedelta(days=7)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Your invoice #INV-567 for $2,450.00 is attached and due on June 30.',
            'body_text': 'Your invoice #INV-567 for $2,450.00 is attached and due on June 30. Please remit payment to the account details listed on the invoice. For any billing inquiries, please contact our finance department.',
            'labels': ['INBOX', 'CATEGORY_PERSONAL', 'UNREAD']
        },
        {
            'id': '9',
            'thread_id': '9',
            'subject': 'Weekend sale - 40% off everything',
            'sender': 'marketing@retailer.com',
            'date': (datetime.now() - timedelta(days=2)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Don\'t miss our biggest sale of the season! 40% off everything this weekend only.',
            'body_text': 'Don\'t miss our biggest sale of the season! 40% off everything this weekend only. Shop online or in-store from Friday through Sunday. Use code WEEKEND40 at checkout. Exclusions may apply to certain brands.',
            'labels': ['INBOX', 'CATEGORY_PROMOTIONS']
        },
        {
            'id': '10',
            'thread_id': '10',
            'subject': 'Document for review',
            'sender': 'colleague@company.com',
            'date': (datetime.now() - timedelta(days=1)).strftime("%a, %d %b %Y %H:%M:%S"),
            'snippet': 'Please review the attached proposal document before Friday\'s meeting.',
            'body_text': 'Please review the attached proposal document before Friday\'s meeting. I\'ve incorporated the changes we discussed last week and added the new budget estimates. Let me know if you have any feedback or suggestions for improvement.',
            'labels': ['INBOX', 'CATEGORY_PERSONAL', 'UNREAD', 'IMPORTANT']
        }
    ]
    return sample_emails

def format_date_range(days_ago=7):
    """Format a date range query string for Gmail API."""
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    
    # Format for Gmail query: after:YYYY/MM/DD before:YYYY/MM/DD
    start_str = start_date.strftime("%Y/%m/%d")
    end_str = end_date.strftime("%Y/%m/%d")
    
    return f"after:{start_str} before:{end_str}"

def extract_query_parameters(query):
    """Extract parameters from natural language query.
    
    This is a simple implementation that could be expanded with more NLP.
    """
    query = query.lower()
    params = {
        "time_period": None,
        "sender": None,
        "has_attachment": False,
        "is_unread": False,
        "label": None
    }
    
    # Check for time periods
    if "today" in query:
        params["time_period"] = 1
    elif "yesterday" in query:
        params["time_period"] = 2
    elif "this week" in query or "last week" in query:
        params["time_period"] = 7
    elif "this month" in query or "last month" in query:
        params["time_period"] = 30
    
    # Check for attachment mentions
    if any(word in query for word in ["attachment", "file", "document", "attached"]):
        params["has_attachment"] = True
    
    # Check for unread mentions
    if "unread" in query:
        params["is_unread"] = True
    
    # Common email labels/categories
    labels = ["inbox", "sent", "draft", "spam", "trash", "important", 
              "primary", "social", "promotions", "updates", "forums"]
    
    for label in labels:
        if label in query:
            params["label"] = label
            break
    
    return params
