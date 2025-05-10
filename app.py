import os
import streamlit as st
import time
import json
from gmail_service import GmailService
from rag_engine import RAGEngine
from utils import save_uploaded_file, get_sample_emails

st.set_page_config(
    page_title="Gmail RAG Assistant",
    page_icon="📬",
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Gmail assistant. I can help you query your emails using natural language. Upload your Gmail API credentials to get started."}
    ]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "gmail_service" not in st.session_state:
    st.session_state.gmail_service = None

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None

if "email_count" not in st.session_state:
    st.session_state.email_count = 0

def authenticate_gmail():
    """Handle Gmail authentication process"""
    try:
        credentials_file = "credentials.json"
        st.session_state.gmail_service = GmailService(credentials_file)
        user_info = st.session_state.gmail_service.get_user_profile()
        
        st.session_state.authenticated = True
        st.session_state.messages.append(
            {"role": "assistant", "content": f"Successfully connected to Gmail account: {user_info['emailAddress']}. I'm now indexing your emails..."}
        )
        
        # Initialize RAG engine with Gmail service
        st.session_state.rag_engine = RAGEngine(st.session_state.gmail_service)
        
        # Fetch and index emails
        with st.spinner("Indexing your emails... This may take a few minutes depending on your inbox size."):
            try:
                email_count = st.session_state.rag_engine.index_emails(limit=100)  # Index the most recent 100 emails
                st.session_state.email_count = email_count
                
                if email_count > 0:
                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"Indexed {email_count} emails. You can now ask questions about your emails!"}
                    )
                else:
                    st.session_state.messages.append(
                        {"role": "assistant", "content": "No emails were found or indexed. Please check your Gmail account and try again."}
                    )
            except Exception as e:
                st.error(f"Error indexing emails: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"There was an error indexing your emails: {str(e)}. You may still try asking questions, but results might be limited."}
                )
        
        st.rerun()
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# Main app layout
st.title("📬 Gmail RAG Assistant")

# Sidebar for authentication and settings
with st.sidebar:
    st.header("Authentication")
    
    if not st.session_state.authenticated:
        st.write("Upload your Google API credentials file to connect to Gmail:")
        credentials_file = st.file_uploader("Upload credentials.json", type=["json"])
        
        # Option to use demo mode with sample data
        use_demo = st.checkbox("Use demo mode with sample data")
        
        if use_demo:
            if st.button("Connect with Sample Data"):
                try:
                    # Initialize RAG engine with sample email data
                    st.session_state.authenticated = True
                    st.session_state.messages.append(
                        {"role": "assistant", "content": "Connected in demo mode with sample email data. You can now ask questions about the sample emails!"}
                    )
                    
                    # Get sample emails and set up RAG engine directly
                    try:
                        sample_emails = get_sample_emails()
                        st.session_state.rag_engine = RAGEngine(None)  # No Gmail service in demo mode
                        st.session_state.rag_engine.emails = sample_emails
                        
                        # Create a FAISS index with the sample emails
                        email_count = st.session_state.rag_engine._create_index_from_samples(sample_emails)
                        st.session_state.email_count = email_count
                        st.success(f"Successfully loaded {email_count} sample emails for demo mode")
                    except Exception as e:
                        st.error(f"Error setting up demo mode: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to initialize demo mode: {str(e)}")
        
        elif credentials_file is not None:
            # Save the uploaded credentials file
            save_uploaded_file(credentials_file, "credentials.json")
            
            if st.button("Connect to Gmail"):
                authenticate_gmail()
    else:
        st.success(f"✅ Connected to Gmail")
        st.write(f"Indexed emails: {st.session_state.email_count}")
        
        if st.button("Refresh Email Index"):
            with st.spinner("Refreshing email index..."):
                email_count = st.session_state.rag_engine.index_emails(limit=100, force_refresh=True)
                st.session_state.email_count = email_count
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"Refreshed index with {email_count} emails."}
                )
                st.rerun()
                
        if st.button("Logout"):
            # Clear session state and remove token file
            if os.path.exists("token.json"):
                os.remove("token.json")
            st.session_state.authenticated = False
            st.session_state.gmail_service = None
            st.session_state.rag_engine = None
            st.session_state.messages = [
                {"role": "assistant", "content": "You've been logged out. Upload your credentials again to reconnect."}
            ]
            st.rerun()
    
    st.header("Sample Questions")
    sample_questions = [
        "What emails did I receive from Amazon last week?",
        "Summarize the last 5 unread messages.",
        "Do I have any emails from my boss this month?",
        "Find emails with attachments from the last 10 days.",
        "What are the most recent emails in my Primary folder?"
    ]
    
    for q in sample_questions:
        if st.button(q):
            st.session_state.messages.append({"role": "user", "content": q})
            if st.session_state.authenticated and st.session_state.rag_engine:
                try:
                    with st.spinner("Thinking..."):
                        response = st.session_state.rag_engine.query(q)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error processing query: {str(e)}"
                    st.error(error_msg)
                    import traceback
                    st.code(traceback.format_exc())
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                st.session_state.messages.append(
                    {"role": "assistant", "content": "Please connect to Gmail first!"}
                )
            st.rerun()

# Chat interface
st.header("Chat with your Gmail")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your emails..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Only process if authenticated
    if st.session_state.authenticated and st.session_state.rag_engine:
        try:
            with st.spinner("Searching your emails..."):
                response = st.session_state.rag_engine.query(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            st.error(error_msg)
            import traceback
            st.code(traceback.format_exc())
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    else:
        st.session_state.messages.append(
            {"role": "assistant", "content": "Please connect to Gmail first by uploading your credentials.json file in the sidebar!"}
        )
    st.rerun()
