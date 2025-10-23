# app.py

import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from src.data_sources import get_public_csv, get_supabase_client
from src.storage import insert_supabase_row
from datetime import datetime

# --- Configuration (from st.secrets) ---
AUTH_CONFIG = st.secrets["auth"]

# --- Authentication ---
names = AUTH_CONFIG["names"].split(',')
usernames = AUTH_CONFIG["usernames"].split(',')
passwords = AUTH_CONFIG["passwords"].split(',') # Hashed in prod
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    AUTH_CONFIG["cookie_name"],
    AUTH_CONFIG["signature_key"],
    cookie_expiry_days=30
)

# --- Main App Logic ---
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.title(f"Welcome, {name}!")

    # 1. Remote Data Read (Cached)
    DATA_URL = "https://raw.githubusercontent.com/fivethirtyeight/data/master/airlines/airlines.csv"
    
    st.header("1. Remote Read Example (Cached)")
    try:
        df_airlines = get_public_csv(DATA_URL)
        st.dataframe(df_airlines.head())
        st.line_chart(df_airlines[['arr_delay', 'dep_delay']].mean())
        
    except Exception as e:
        st.error(f"Could not load public data: {e}")
        st.stop()


    # 2. Remote Data Write (Form Submission)
    st.header("2. Remote Write Example (Supabase)")
    
    with st.form("feedback_form"):
        st.markdown("Submit anonymous feedback on this app.")
        feedback_text = st.text_area("Your Feedback", max_chars=500)
        rating = st.slider("Rating", 1, 5, 5)
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            data = {
                "timestamp": datetime.now().isoformat(),
                "user_id": username, # Logged-in user
                "rating": rating,
                "feedback": feedback_text
            }
            try:
                insert_supabase_row("feedback", data)
                st.success("Thank you for your feedback! Data written to remote Supabase.")
            except Exception as e:
                st.error(f"Failed to write to remote store. Check Supabase connection/table schema. Error: {e}")
                st.exception(e)

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')

# 3. Guardrail Check (Informational)
st.sidebar.info("This application operates with a **No-Local-Files** policy. All data is fetched from and persisted to remote services (GitHub Raw, Supabase).")
