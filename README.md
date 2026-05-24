# 🤖 AI Chatbot — Groq API

**Batch E2 (TFS) · AI/ML Internship · Assignment 3**

A full-featured AI chatbot built with Streamlit and powered by Groq's ultra-fast LLM inference API. Supports multi-turn conversations, PDF document Q&A, and voice input via Groq Whisper.

---

## ✨ Features

- **Multi-model support** — Switch between LLaMA, Gemma, and Mixtral models
- **Chat history** — Create, switch, rename, and delete multiple chat sessions
- **PDF Q&A** — Upload a PDF and ask questions from its content
- **Voice input** — Speak your message using the built-in mic recorder
- **Custom system prompt** — Configure the AI's personality and behavior
- **Persistent conversation** — Full conversation history sent with every request

---

## 🧠 Models Available

| Model | Description |
|---|---|
| `llama-3.1-8b-instant` | Fast, lightweight — best for quick responses |
| `llama-3.3-70b-versatile` | Most capable LLaMA model |
| `gemma2-9b-it` | Google's Gemma 2 instruction-tuned |
| `mixtral-8x7b-32768` | Large context window (32K tokens) |

---

## 🗂️ Project Structure

```
chatbot-project/
│
├── app.py           ← Main Streamlit UI
├── chatbot.py       ← Groq API logic (chat + voice + PDF)
├── test_groq.py     ← Quick API connection test
├── requirements.txt
└── .env             ← API keys (never commit this)
```

---

## ⚙️ How It Works

```
User types / speaks
       ↓
app.py collects input
       ↓
chatbot.py → Groq API (LLM)
       ↓
AI reply streamed back
       ↓
Displayed in chat UI
```

**PDF Q&A flow:**
```
User uploads PDF
       ↓
PyPDF2 extracts text
       ↓
Text injected into system prompt
       ↓
AI answers from document context
```

**Voice flow:**
```
User records audio (mic_recorder)
       ↓
Audio bytes → Groq Whisper (whisper-large-v3)
       ↓
Transcribed text → sent as chat message
```

---

## 🚀 Setup & Installation

### 1. Clone the project

```bash
git clone https://github.com/yourusername/ai-chatbot-groq.git
cd ai-chatbot-groq
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key

### 4. Create `.env` file

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Test your API connection

```bash
python test_groq.py
```

Expected output:
```
✅ Groq API is working!
Response: Hello! How can I help you today?
```

### 6. Run the app

```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 📦 Requirements

```
streamlit
openai
groq
python-dotenv
PyPDF2
streamlit-mic-recorder
```

Install all at once:

```bash
pip install streamlit openai groq python-dotenv PyPDF2 streamlit-mic-recorder
```

---

## 🖥️ Usage Guide

### Basic Chat
1. Open the app at `http://localhost:8501`
2. Type your message in the chat box at the bottom
3. Press Enter — AI replies instantly

### Switch Models
- Open the **sidebar → Settings → Choose Model**
- Select any model from the dropdown
- Continue chatting — new model applies to next message

### PDF Q&A
1. Sidebar → **PDF Q&A → Upload a PDF**
2. Wait for "✅ PDF loaded!" confirmation
3. Ask questions about the document in the chat
4. AI answers from document content for related questions, general knowledge for others

### Voice Input
1. Click **🎙️ Click to speak**
2. Speak your message clearly
3. Click **⏹️ Stop recording**
4. Wait for transcription — message sends automatically

### Multiple Chats
- Click **➕ New Chat** to start a fresh conversation
- Click any chat in history to switch to it
- Click 🗑 next to any chat to delete it
- Click **🗑️ Clear Chat** button to clear current chat messages

### Custom System Prompt
- Sidebar → **Settings → System Prompt**
- Edit the text area to change AI behavior
- Example: `"You are a Python tutor. Only answer Python-related questions."`

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com | ✅ Yes |

---

## 📁 File Details

### `app.py`
Main Streamlit application. Handles:
- Page layout and dark sidebar UI
- Session state for all chat sessions
- Voice recording via `streamlit-mic-recorder`
- PDF upload and system prompt injection
- Chat rendering and input processing

### `chatbot.py`
Core logic layer. Contains three functions:
- `get_response(conversation, model)` — sends conversation to Groq, returns reply
- `transcribe_audio(audio_bytes)` — sends audio to Groq Whisper, returns text
- `extract_pdf_text(uploaded_file)` — reads PDF with PyPDF2, returns raw text

### `test_groq.py`
Standalone script to verify your API key and connection work before running the full app.

---

## 🐛 Common Issues & Fixes

| Problem | Fix |
|---|---|
| `GROQ_API_KEY not found` | Check `.env` file exists and key is correct |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Voice not working | Allow microphone access in browser settings |
| PDF not loading | Try a text-based PDF (not scanned images) |
| Model error | Check [Groq model availability](https://console.groq.com/docs/models) |
| Slow responses | Switch to `llama-3.1-8b-instant` for faster replies |

---

## 📊 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Web UI framework |
| Groq API | LLM inference (ultra-fast) |
| OpenAI SDK | Used as Groq-compatible client |
| Groq SDK | Used for Whisper audio transcription |
| PyPDF2 | PDF text extraction |
| streamlit-mic-recorder | In-browser microphone recording |
| python-dotenv | Environment variable management |

---

## 👨‍💻 Author

**Your Name**
Gaurav Sharma 

---

## 📄 License

This project is built for educational purposes as part of an AI/ML internship program.
