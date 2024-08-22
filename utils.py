from collections import Counter
from deep_translator import GoogleTranslator
import spacy
from spacy.lang.en import English

def translate_text(text, target_language='en'):
    return GoogleTranslator(source='auto', target=target_language).translate(text)

def analyze_text(text):
    words = text.lower().split()
    return dict(Counter(words))  

def transcribe_audio(audio_data):
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

# Load the spaCy English tokenizer
nlp = English()

def get_top_unique_phrases(text, n=3):
    doc = nlp(text.lower())
    words = [token.text for token in doc]

    # Generate trigrams (or other n-grams)
    trigrams = zip(words, words[1:], words[2:])
    trigram_freq = Counter(trigrams)

    # Get the top n most common trigrams
    most_common_phrases = trigram_freq.most_common(n)

    # Join the words in each trigram to form phrases
    return [' '.join(phrase) for phrase, _ in most_common_phrases]
