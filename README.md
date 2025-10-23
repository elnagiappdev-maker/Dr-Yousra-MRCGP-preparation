# Cloud-Hosted Streamlit App: No Local Machine

This repository is designed for 100% cloud development via GitHub Codespaces or the GitHub Web Editor, and deployment via Streamlit Community Cloud. All data persistence is remote (Supabase/Sheets/Firestore).

## 🚀 Quick Deployment Guide (Web UI Only)

1.  **Fork/Clone:** Ensure this repository is in your GitHub account.
2.  **Create Secrets:** Get your Supabase/Google Service Account credentials ready. **DO NOT COMMIT THEM.**
3.  **Deploy to Streamlit Cloud:**
    *   Go to [Streamlit Community Cloud](https://share.streamlit.io/).
    *   Click **"New app"** -> Select this repository, `main` branch, and `app.py`.
    *   Click **"Advanced settings"** -> **"Edit secrets"**.
    *   Copy the content of `.streamlit/secrets.toml.example` (filled with your **real** secrets) and paste it into the Streamlit Cloud Secrets box.
    *   Click **"Deploy!"**
4.  **Verify CI:** Check the "Actions" tab in GitHub to ensure the `ci.yml` workflow passes (linting and the "No Local Write" Guardrail).

## 🛡️ No Local Write Guardrail

This application strictly prohibits writing files to the local disk of the Streamlit Cloud server. All persistence must be remote. The GitHub CI automatically checks for file write patterns (`open(..., 'w')`) and will fail the build if a violation is detected. Use `io.BytesIO` for in-memory handling of temporary data (e.g., charts).
