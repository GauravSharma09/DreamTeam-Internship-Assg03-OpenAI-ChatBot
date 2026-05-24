import streamlit as st
from chatbot import get_response, extract_pdf_text, transcribe_audio
from streamlit_mic_recorder import mic_recorder
import datetime

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #0f1117;
    }
    .stButton > button {
        border-radius: 8px;
        font-size: 13px;
    }
    .welcome-box {
        text-align: center;
        padding: 80px 0;
        color: #8892aa;
    }
    .welcome-box .icon { font-size: 52px; }
    .welcome-box .title {
        font-size: 22px;
        font-weight: 700;
        margin: 14px 0 8px;
        color: #e8eaf0;
    }
    .welcome-box .sub { font-size: 14px; }
    .voice-box {
        background: #1c2030;
        border: 1px solid #2a2f42;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ── Session State Init ─────────────────────────────────────────
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are a helpful and friendly AI assistant. "
        "Answer clearly and concisely."
    )

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""


# ── Helper Functions ───────────────────────────────────────────
def create_new_chat():
    chat_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.all_chats[chat_id] = {
        "title": "New Chat",
        "messages": [],
        "created": datetime.datetime.now().strftime("%d %b, %I:%M %p")
    }
    st.session_state.current_chat_id = chat_id


def get_current_messages():
    if st.session_state.current_chat_id:
        return st.session_state.all_chats[
            st.session_state.current_chat_id
        ]["messages"]
    return []


def update_chat_title(chat_id, first_message):
    title = (
        first_message[:28] + "..."
        if len(first_message) > 28
        else first_message
    )
    st.session_state.all_chats[chat_id]["title"] = title


# Create first chat on startup
if st.session_state.current_chat_id is None:
    create_new_chat()


# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:

    if st.button("➕  New Chat", use_container_width=True, type="primary"):
        create_new_chat()
        st.rerun()

    st.divider()

    st.markdown("#### 💬 Chat History")

    if st.session_state.all_chats:
        sorted_chats = sorted(
            st.session_state.all_chats.items(),
            key=lambda x: x[0],
            reverse=True
        )

        for chat_id, chat_data in sorted_chats:
            is_active = chat_id == st.session_state.current_chat_id
            col1, col2 = st.columns([5, 1])

            with col1:
                label = (
                    f"🟦 {chat_data['title']}"
                    if is_active
                    else f"⬜ {chat_data['title']}"
                )
                if st.button(label, key=f"chat_{chat_id}",
                             use_container_width=True):
                    st.session_state.current_chat_id = chat_id
                    st.rerun()

            with col2:
                if st.button("🗑", key=f"del_{chat_id}"):
                    del st.session_state.all_chats[chat_id]
                    if st.session_state.current_chat_id == chat_id:
                        if st.session_state.all_chats:
                            st.session_state.current_chat_id = list(
                                st.session_state.all_chats.keys()
                            )[-1]
                        else:
                            create_new_chat()
                    st.rerun()
    else:
        st.caption("No chats yet.")

    st.divider()

    st.markdown("#### ⚙️ Settings")

    model_choice = st.selectbox(
        "Choose Model",
        [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ]
    )

    custom_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful and friendly AI assistant. Answer clearly and concisely.",
        height=100
    )

    st.divider()

    st.markdown("#### 📄 PDF Q&A")
    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_pdf is not None:
        pdf_text = extract_pdf_text(uploaded_pdf)
        if pdf_text:
            st.success(f"✅ PDF loaded! ({len(pdf_text)} chars)")
            st.session_state.pdf_uploaded = True
            st.session_state.system_prompt = f"""You are a helpful and friendly AI assistant.

You have been given an uploaded document by the user. Follow these rules:

1. If the user asks a question RELATED to the document → answer using the document content below.
2. If the user asks a GENERAL question not related to the document → answer it normally using your own knowledge.
3. NEVER say you cannot access files. The document is already extracted and given to you.
4. NEVER say "the document doesn't contain information" for general knowledge questions. Just answer them.
5. Be helpful, clear, and friendly at all times.

--- DOCUMENT CONTENT START ---
{pdf_text[:6000]}
--- DOCUMENT CONTENT END ---"""
        else:
            st.error("❌ Could not read this PDF. Try another file.")
            st.session_state.pdf_uploaded = False
    else:
        st.session_state.pdf_uploaded = False
        st.session_state.system_prompt = custom_prompt

    if st.session_state.pdf_uploaded:
        st.info("🤖 Bot answers both PDF & general questions.")

    st.caption("Built by: Your Name | AI/ML Internship")


# ── Main Area ──────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])

with col1:
    st.title("🤖 AI Chatbot")
    st.caption(f"Groq · {model_choice} | Assignment 3 – Batch E2 (TFS)")

with col2:
    st.write("")
    st.write("")
    if st.button("🗑️ Clear Chat"):
        if st.session_state.current_chat_id:
            st.session_state.all_chats[
                st.session_state.current_chat_id
            ]["messages"] = []
            st.session_state.all_chats[
                st.session_state.current_chat_id
            ]["title"] = "New Chat"
        st.rerun()

st.divider()

# ── Chat Messages ──────────────────────────────────────────────
messages = get_current_messages()

if not messages:
    st.markdown("""
    <div class="welcome-box">
        <div class="icon">🤖</div>
        <div class="title">How can I help you today?</div>
        <div class="sub">
            Type or speak below · Upload a PDF from sidebar for document Q&A
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# ── Voice Input ────────────────────────────────────────────────
st.markdown("#### 🎙️ Voice Input")

with st.container():
    st.markdown('<div class="voice-box">', unsafe_allow_html=True)

    audio = mic_recorder(
        start_prompt="🎙️ Click to speak",
        stop_prompt="⏹️ Stop recording",
        just_once=True,
        use_container_width=True,
        key="voice_recorder"
    )

    # If audio recorded — transcribe it
    if audio and audio.get("bytes"):
        with st.spinner("🔄 Transcribing voice..."):
            transcribed = transcribe_audio(audio["bytes"])

        if transcribed and not transcribed.startswith("❌"):
            st.success(f"✅ You said: **{transcribed}**")
            st.session_state.voice_text = transcribed
        else:
            st.error(transcribed)

    st.markdown('</div>', unsafe_allow_html=True)


# ── Text Input ─────────────────────────────────────────────────
user_input = st.chat_input("Type your message here...")

# Use voice text if available, else use typed text
final_input = None

if st.session_state.voice_text:
    final_input = st.session_state.voice_text
    st.session_state.voice_text = ""   # clear after use

elif user_input:
    final_input = user_input


# ── Process Input ──────────────────────────────────────────────
if final_input:
    chat_id = st.session_state.current_chat_id
    messages = get_current_messages()

    if len(messages) == 0:
        update_chat_title(chat_id, final_input)

    messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.markdown(final_input)

    conversation = [{"role": "system", "content": st.session_state.system_prompt}]
    conversation += messages

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_response(conversation, model=model_choice)
        st.markdown(reply)

    messages.append({"role": "assistant", "content": reply})
    st.rerun()


    #python -m streamlit run app.py