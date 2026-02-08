# 🚀 AI Code Reviewer (Streamlit + Groq / Ollama)

**AI-powered code review tool** that scans repositories or single files and provides structured feedback using:

- **Static analysis** (Python AST + generic file checks)  
- **AI-based review** via **Groq API (online)** or **Ollama (offline)**  

This tool helps developers quickly identify **bad practices, security risks, long functions, hardcoded secrets**, and provides actionable suggestions.

---

## ✨ Features

- Upload a **repository ZIP** or a **single file**  
- Detect common issues:
  - Long functions  
  - Hardcoded passwords or secrets  
- **AI Review Modes**:
  - **Junior** → friendly, educational explanations  
  - **Senior** → strict, production-ready feedback  
- Supports multiple languages:
  - Python, JavaScript/TypeScript, C/C++, Java, PHP, Go, Rust  
  - HTML, CSS, SQL, shell scripts  

---

## 🛠️ Tech Stack

- **Python 3.11**  
- **Streamlit** (UI)  
- **AST Parsing** (static analysis)  
- **Groq API** (online LLM)  
- **Ollama** (offline LLM)  
- **Requests** (API calls)  

---

## ⚡ Setup Instructions

### 1. Clone Repository
```bash
git clone <repository-url>
cd AI-Code-Reviewer
2. Install Dependencies
bash
Copy code
pip install -r requirements.txt
3. Create .env File
env
Copy code
# Optional: Groq API Key (required for online mode)
GROK_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx

# Ollama server URL (required for offline mode)
OLLAMA_API_URL=http://localhost:11434
Keep this file private. Do not commit to version control.

4. (Optional) Offline Ollama Setup
Install Ollama: https://ollama.com

Download the deepseek-coder:6.7b model locally

Start Ollama server:

bash
Copy code
ollama serve
5. Run the Streamlit Application
bash
Copy code
streamlit run app.py
Open your browser at http://localhost:8501

Upload a ZIP repository or a single file

Select Reviewer Mode (Junior / Senior)

Select LLM Provider (Auto / Groq / Ollama)

Click Review Code to see static analysis + AI review

📝 Usage Notes

Offline Ollama mode is recommended for large repositories.

Ensure the Ollama server is running when using offline mode.

Only supported file types are scanned (refer to project structure).


