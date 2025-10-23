# src/data_sources.py
import pandas as pd
import requests
import streamlit as st
from supabase import create_client, Client
from google.oauth2 import service_account
import gspread

# --- Client Factories (Use st.cache_resource for long-lived connections) ---

@st.cache_resource(ttl=None) # Cache resource for the lifetime of the app process
def get_supabase_client() -> Client:
    """Connects to Supabase using st.secrets."""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error("Error connecting to Supabase. Check secrets configuration.")
        st.exception(e)
        raise

@st.cache_resource(ttl=None)
def get_gspread_client():
    """Authenticates gspread using the Streamlit Cloud secrets for a service account."""
    try:
        # Load service account JSON from secrets
        gs_creds = st.secrets["google_service_account"]
        
        # Create credentials object
        credentials = service_account.Credentials.from_service_account_info(
            info=gs_creds, 
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        return gspread.authorize(credentials)
    except Exception as e:
        st.error("Error connecting to Google Sheets. Check service account credentials and permissions.")
        st.exception(e)
        raise

# --- Data Fetchers ---

@st.cache_data(ttl=300) # Cache for 5 minutes
def get_public_csv(url: str) -> pd.DataFrame:
    """Fetches a public CSV from a URL (e.g., GitHub Raw)."""
    try:
        return pd.read_csv(url, on_bad_lines='skip')
    except Exception as e:
        st.error(f"Failed to fetch CSV from URL: {url}")
        st.exception(e)
        raise

@st.cache_data(ttl=300)
def get_json(url: str) -> dict:
    """Fetches public JSON data."""
    try:
        response = requests.get(url)
        response.raise_for_status() # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch JSON from URL: {url}")
        st.exception(e)
        raise
