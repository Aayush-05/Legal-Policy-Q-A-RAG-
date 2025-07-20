# Legal Policy Q&A (RAG)

A Retrieval-Augmented Generation (RAG) pipeline for answering legal questions using company policy PDFs (Amazon, Instagram, Meta, Bennett University, etc.).
<img width="1598" height="961" alt="Screenshot 2025-07-20 at 5 56 56 PM" src="https://github.com/user-attachments/assets/57098337-5bd2-4650-a666-dfbed887456b" />


## Features
- Loads and vectorizes PDFs from `documents/` using LangChain, FAISS, and HuggingFace sentence embeddings
- FastAPI backend with `/ask` endpoint
- Streamlit UI for interactive Q&A
- Uses Claude 3 Sonnet LLM API for context-aware answers

## Setup
1. **Clone the repo and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Add your Claude API key:**
   - Create a `.env` file in the project root and add:
     ```
     CLAUDE_API_KEY=your-claude-api-key-here
     ```
3. **Ensure you have the required PDFs in the `documents/` folder.**

## Running Locally
1. **Start the FastAPI backend:**
   ```bash
   uvicorn main:app --reload
   ```
2. **Start the Streamlit UI:**
   ```bash
   streamlit run ui.py
   ```

## Deployment
1. **Choose a server or cloud platform** (AWS EC2, GCP, Azure, DigitalOcean, Render, Railway, Heroku, etc.)
2. **Install Python 3.8+ and dependencies** as above.
3. **Set up your `.env` and upload PDFs** as above.
4. **Run the backend:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
5. **Run the Streamlit UI:**
   ```bash
   streamlit run ui.py
   ```
6. **(Optional) Use a process manager** (systemd, pm2, etc.) or Docker for production reliability.
7. **(Optional) Set up a reverse proxy** (e.g., Nginx) for public access.

## Environment Variables
- `CLAUDE_API_KEY`: Your Claude LLM API key

## Notes
- Requires Python 3.8+
- Add `.env` and `.DS_Store` to your `.gitignore`
