import os
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "llama-3.1-8b-instant"

# Client for chat
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Client for voice transcription
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_response(conversation_history, model=GROQ_MODEL):
    """Send conversation to Groq and return AI reply."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"


def transcribe_audio(audio_bytes):
    """Convert voice audio bytes to text using Groq Whisper."""
    try:
        import tempfile

        # Save audio bytes to a temp file
        with tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False
        ) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        # Send to Groq Whisper
        with open(tmp_path, "rb") as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=("audio.wav", audio_file, "audio/wav"),
                model="whisper-large-v3",
                language="en"
            )

        # Clean up temp file
        os.remove(tmp_path)
        return transcription.text

    except Exception as e:
        return f"❌ Voice error: {str(e)}"


def extract_pdf_text(uploaded_file):
    """Extract all text from an uploaded PDF file."""
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"