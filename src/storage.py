# src/storage.py
import pandas as pd
from src.data_sources import get_supabase_client, get_gspread_client
# from google.cloud import firestore # Uncomment for Firestore

# --- Supabase (Preferred Write Example) ---

def insert_supabase_row(table_name: str, data: dict):
    """Inserts a single row into a Supabase table."""
    try:
        supabase = get_supabase_client()
        # Use execute() for simplicity, or table() for query builder
        response = supabase.table(table_name).insert(data).execute()
        
        if response.data is None and response.error:
            raise Exception(response.error.message)
            
    except Exception as e:
        st.error(f"Supabase INSERT failed for table '{table_name}'.")
        raise Exception(f"Supabase Write Error: {e}")

# --- Google Sheets (Alternative Write Example) ---
def append_to_gsheet(sheet_id: str, worksheet_name: str, row_data: list):
    """Appends a row to a specific Google Sheet worksheet."""
    try:
        client = get_gspread_client()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        worksheet.append_row(row_data)
    except Exception as e:
        st.error("Google Sheets APPEND failed. Check sheet ID, worksheet name, and service account sharing permissions.")
        raise Exception(f"GSheet Write Error: {e}")

# --- Firebase/Firestore (Alternative Write Example) ---
# def upsert_firestore_doc(collection_name: str, document_id: str, data: dict):
#     """Sets/updates a document in a Firestore collection."""
#     try:
#         # Need a separate client factory for Firestore using google-cloud-firestore 
#         # and st.secrets for authentication.
#         db = firestore.Client(credentials=get_firestore_creds(), project=st.secrets["google_service_account"]["project_id"])
#         db.collection(collection_name).document(document_id).set(data)
#     except Exception as e:
#         st.error("Firestore UPSERT failed.")
#         raise Exception(f"Firestore Write Error: {e}")
