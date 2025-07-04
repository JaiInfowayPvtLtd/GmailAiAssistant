# USA Mountain Trekking Guide - Installation Guide

This document provides step-by-step instructions to set up and run the USA Mountain Trekking Guide application on your local machine.

## Prerequisites

Before installing the application, make sure you have the following installed:

- Python 3.9+
- pip (Python package installer)
- OpenAI API Key (required for AI functionality)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/usa-mountain-trekking-guide.git
cd usa-mountain-trekking-guide
```

### 2. Create a requirements.txt File

If not already present, create a `requirements.txt` file and add the following content. These include mandatory dependencies and others derived from pyproject.toml:

```txt
##--Below are mendatory code that should be on the requirements.txt file 
Flask
gunicorn==20.1.0
sib-api-v3-sdk==7.6.0

##---Below are dependecies of .toml file as example. you should put your own dependecies from .toml file.
beautifulsoup4>=4.13.4
faiss-cpu>=1.11.0
google-api-python-client>=2.169.0
google-auth>=2.40.1
google-auth-oauthlib>=1.2.2
numpy>=2.2.5
openai>=1.78.0
python-dotenv>=1.1.0
streamlit>=1.45.0
```

### 3. Create a Virtual Environment

Create an isolated Python environment to manage dependencies separately from your system Python.

```bash
# Create a virtual environment named .venv using Python 3.12. ,,,,3.12 is pythone version (use it your accordingly)
python3.12 -m venv .venv
```

This command initializes a virtual environment in the `.venv` directory using Python 3.12.

### 4. Activate the Virtual Environment

Activate the virtual environment to begin installing and running packages within it:

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows (use in CMD)
.venv\Scripts\activate
```

### 5. Install Dependencies

Install all required Python libraries listed in requirements.txt:

```bash
pip install -r requirements.txt
```

This command reads the file and installs all listed packages inside your virtual environment.

### 6. Provide Your OpenAI API Key

The application uses OpenAI services, so you must provide your API key.

**Option 1: Export the API key in the shell**

```bash
export OPENAI_API_KEY="your-api-key-here"
```

This makes the API key available as an environment variable during your terminal session.

> **Important:** Replace the example key with your actual OpenAI API key.

### 7. Activate Environment (If Not Already Active)

Ensure the virtual environment is active before running the application:

```bash
source .venv/bin/activate
```

### 8. Start the Application

Launch the Streamlit app:

```bash
streamlit run app.py
```

This command starts the server and opens the application in your browser at http://localhost:8501 or may be in another server.

## Configuration Options

Modify `.streamlit/config.toml` to change server settings:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Troubleshooting

### API Key Issues
- Ensure your OpenAI API key is valid and correctly exported
- Check your usage limits or subscription status if errors occur

### Dependencies
- Update all packages if needed:
  ```bash
  pip install --upgrade -r requirements.txt
  ```
- Ensure you're using Python 3.9 or later

### Map Issues
- Check internet connection
- Confirm successful installation of folium and streamlit-folium

## Deployment Options

### Streamlit Cloud
1. Push your code to GitHub
2. Sign in at Streamlit Cloud
3. Connect your repository
4. Add your API key as a secret
5. Deploy with one click

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "5000"]
```

Build and run:

```bash
docker build -t mountain-trekking-guide .
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key_here mountain-trekking-guide
```
