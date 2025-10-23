# Deployment Walkthrough: Streamlit Community Cloud

This guide assumes you have pushed all files (`app.py`, `requirements.txt`, etc.) to the `main` branch of your GitHub repository.

## Step 1: Prepare Secrets

1.  Open your local copy of `.streamlit/secrets.toml.example`.
2.  Fill in the real values for `supabase`, `google_service_account`, and `auth`.
3.  **Copy the entire content** of the file (including headers like `[supabase]`).

## Step 2: Deploy

1.  Navigate to the Streamlit Community Cloud dashboard.
2.  Click **"New App"** in the top right corner.
3.  In the deployment window:
    *   **Repository:** Select your GitHub repository.
    *   **Branch:** Set to `main`.
    *   **Main file path:** Set to `app.py`.
4.  Click the **"Advanced settings"** dropdown.
5.  Click the **"Edit secrets"** button.
6.  **Paste the full content** from Step 1 into the secrets text area.
7.  Click **"Save secrets"**.
8.  Click **"Deploy!"**.

## Troubleshooting Deployment

*   **Dependency Failure:** If the app fails on `pip install`, check `requirements.txt` for typos or unpinned, volatile versions.
*   **Secrets Error:** If the app runs but fails on remote calls, check the application logs in the Streamlit Cloud dashboard. Common error: "KeyError: 'supabase'". This usually means the TOML format was incorrect when pasting, or the key name in the app code is wrong.
*   **Permissions:** For Google Sheets/Supabase, ensure the Service Account (Sheets) or the API Key (Supabase) has the necessary **write permissions** and that the sheets/tables are shared/configured correctly.
