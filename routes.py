from flask import Blueprint, request, jsonify, render_template
from models import db, Transcription
from utils import analyze_text, translate_text, transcribe_audio, get_top_unique_phrases
from collections import Counter

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/history')
def history():
    transcriptions = Transcription.query.all()

    # Calculate global word frequency
    global_word_frequency = Counter()
    for transcription in transcriptions:
        global_word_frequency.update(analyze_text(transcription.translated_text))

    return render_template('history.html', transcriptions=transcriptions, global_word_frequency=global_word_frequency, analyze_text=analyze_text)

@bp.route('/upload', methods=['POST'])
def upload():
    try:
        text = request.form.get('text')
        language = request.form.get('language')

        if not text:
            return jsonify({"error": "Text is required"}), 400

        if language != 'en':
            translated_text = translate_text(text)
        else:
            translated_text = text

        transcription = Transcription(text=text, translated_text=translated_text)
        db.session.add(transcription)
        db.session.commit()

        word_frequency = analyze_text(transcription.translated_text)
        top_phrases = get_top_unique_phrases(transcription.translated_text)

        return jsonify({
            'transcription': transcription.translated_text,
            'word_frequency': word_frequency,
            'top_phrases': top_phrases
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
