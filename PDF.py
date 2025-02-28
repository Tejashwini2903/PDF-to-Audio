import fitz  # PyMuPDF for extracting text from PDF
from gtts import gTTS
import os
import platform
import subprocess

# Supported languages
LANGUAGES = {
    "english": "en",
    "hindi": "hi",
    "kannada": "kn",
    "telugu": "te",
    "tamil": "ta",
    "marathi": "mr",
    "bengali": "bn",
    "malayalam": "ml",
    "gujarati": "gu",
    "punjabi": "pa",
    "urdu": "ur",
}

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

# Function to play audio based on OS
def play_audio(file_path):
    system_name = platform.system()
    
    if system_name == "Windows":
        subprocess.run(["start", file_path], shell=True)
    elif system_name == "Darwin":  # macOS
        os.system(f"afplay {file_path}")
    elif system_name == "Linux":
        os.system(f"mpg321 {file_path}")
    else:
        print("❌ Unable to play audio automatically. Please open the file manually.")

# Function to convert text to speech in the chosen language
def text_to_speech_gtts(text, language, output_file="audiobook.mp3"):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save(output_file)
        print(f"✅ Audiobook saved as '{output_file}'")
        play_audio(output_file)
    except Exception as e:
        print(f"❌ Error generating audio: {e}")

# Main function
def main():
    pdf_path = r"C:\Users\mohan\Downloads\resume_itigi_tejashwini (11).pdf"  # Your PDF file path
    
    print("📄 Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ No text found in PDF.")
        return

    # Auto-detect English and convert directly
    if text.isascii():
        print("📝 Detected English text. Converting to English audiobook...")
        text_to_speech_gtts(text, "en")
    else:
        # Display language options for translation
        print("\n🌍 Available Languages:")
        for i, (lang_name, lang_code) in enumerate(LANGUAGES.items(), 1):
            print(f"{i}. {lang_name.capitalize()}")

        # Get user input for language choice
        lang_choice = input("\n🔹 Enter the language name (e.g., hindi, kannada, tamil): ").strip().lower()
        
        if lang_choice in LANGUAGES:
            language_code = LANGUAGES[lang_choice]
            print(f"🎙️ Converting text to speech in {lang_choice.capitalize()}...")
            text_to_speech_gtts(text, language_code)
        else:
            print("❌ Invalid language choice. Please restart and select a valid language.")

if __name__ == "__main__":
    main()
