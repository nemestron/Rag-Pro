# Deployment Guide

RAG Pro is designed to be easily deployable to cloud environments, with Streamlit Community Cloud being the recommended hosting provider for portfolio demonstration.

## Deploying to Streamlit Community Cloud

1. **GitHub Preparation**: Ensure your repository is public and all dependencies are correctly listed in `requirements.txt`.
2. **Account Setup**: Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3. **Deploy App**:
   * Click "New app".
   * Select the `Rag-Pro` repository.
   * Set the branch to `main`.
   * Set the Main file path to `app/main.py`.
4. **Environment Variables (Crucial)**:
   * Before clicking deploy, click on "Advanced settings".
   * In the "Secrets" field, add your Hugging Face API key:
     ```toml
     HUGGINGFACEHUB_API_TOKEN="your_actual_token_here"
     ```
5. **Launch**: Click "Deploy". The platform will automatically install the packages from `requirements.txt` and launch the application.

## Local Docker Deployment (Optional)
To containerize this application, create a standard `Dockerfile` exposing port 8501, and define the `ENTRYPOINT` as `["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]`.
