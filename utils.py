import os
import streamlit as st

def save_uploaded_file(uploaded_file, save_path):
    """Save an uploaded file to the specified path."""
    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return False

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
