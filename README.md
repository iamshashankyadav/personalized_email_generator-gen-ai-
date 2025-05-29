# 📧 AI-Powered Cold Email Generator

Generate personalized cold emails by scraping job descriptions, analyzing tech stacks, and matching your portfolio automatically.

## 🔧 Technologies
- Streamlit UI
- LangChain + LLM (GROQ / Llama 3)
- ChromaDB for vector search
- dotenv for API key handling

## 🛡️ Security
Your API key is never exposed — we use `.env` (local) and `Secrets` (cloud).

## 📁 Setup

```bash
pip install -r requirements.txt
streamlit run app/main.py
