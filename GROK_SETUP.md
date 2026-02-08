# Groq API Setup Guide

## Getting Groq API Credentials

### 1. **Sign Up for Groq**
   - Visit **[console.groq.com](https://console.groq.com)**
   - Create an account (free, no credit card required)

### 2. **Get Your API Key**
   - Navigate to **API Keys** section in the console
   - Click **"Create API Key"**
   - Copy and save your API key (format: starts with `gsk_`)
   - **Keep this secret!** Never commit to git.

### 3. **Update `.env` File**
   That's it! Just add your key:
   ```env
   GROK_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
   ```
   The endpoint URL is hardcoded and automatic.

### 4. **Test Connection** (Optional)
   Run a quick test:
   ```bash
   python -c "from reviewer import review_with_llm; print(review_with_llm('print(1+1)', [], provider='grok'))"
   ```

---

## That's it!
Your code in `reviewer.py` will automatically detect `GROK_API_KEY` and use **Groq** as the provider.

## Available Models
Groq offers several fast models (check for decommissioned ones):
- `llama-3.3-70b-versatile` (current recommended - powerful)
- `llama-3.1-70b-versatile` (alternative)
- Check [console.groq.com/docs](https://console.groq.com/docs) for latest & deprecation info

## Resources
- **Console**: [console.groq.com](https://console.groq.com)
- **Docs**: [Groq API Documentation](https://console.groq.com/docs)
