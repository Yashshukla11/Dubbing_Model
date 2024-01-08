from gtts import gTTS
import os
from googletrans import Translator

# Function to convert text to the target language and save it to a file
def convert_text_to_target_language(text_file, target_language, output_file):
    try:
        # Translate the input text to the selected target language
        with open(text_file, 'r', encoding='utf-8') as file:
            
            text = file.read()
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        translated_text = translated.text

        # Save the translated text to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_text)
    except Exception as e:
        print(f"Error converting text to the target language: {str(e)}")

# Function to convert the target language text file to audio
def convert_text_file_to_audio(text_file, target_language, output_file):
    try:
        # Read the text from the target language text file
        with open(text_file, 'r', encoding='utf-8') as file:
            
            text = file.read()
            
        # Create a gTTS object for the text and save it as audio
        tts = gTTS(text=text, lang=target_language, slow=False)
        tts.save(output_file)  # Save the audio file
    except Exception as e:
        print(f"Error converting text file to audio: {str(e)}")



