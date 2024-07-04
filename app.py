from flask import *
import os
import assemblyai as aai
from gemini import *
import requests
from dotenv import load_dotenv

load_dotenv('.env.local')

ASSEMBLY_AI_API_KEY = os.getenv('ASSEMBLY_AI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
VERTEX_AI_API_KEY= os.getenv('VERTEX_AI_API_KEY')

app = Flask(__name__)

app_data = {'project_name': 'Lucid AI'}
app.secret_key = VERTEX_AI_API_KEY

aai.settings.api_key = ASSEMBLY_AI_API_KEY

@app.route("/")
def index():
    app_data = {'project_name': 'Lucid AI'}
    return render_template("index.html", app_data=app_data)

@app.route('/vision')
def about():
    return render_template('vision.html', app_data=app_data)

@app.route('/success', methods=['POST'])
def success():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "Empty filename"

    global file_path

    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    if file.filename.endswith('.mp3'):
        transcribe_audio(file_path)
        file_path = os.path.join('uploads', file.filename + "transcribed")

    session['file_path'] = file_path

    output = run_python_script(file_path)

    return redirect(url_for('show_output', output=output))

def get_session():
    return session.get('file_path')

def run_python_script(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def transcribe_audio(file_path):
    FILE_URL = file_path
    config = aai.TranscriptionConfig(auto_highlights=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL, config=config)
    transcription_text = transcript.text
    transcribed_file_path = os.path.join(file_path + "transcribed")
    with open(transcribed_file_path, 'w') as file:
        file.write(transcription_text)

    return transcript.text

@app.route('/show_output')
def show_output():
    output = request.args.get('output', '')
    return render_template('output.html', output=output, app_data=app_data)

@app.route('/transcript')
def transcript():
    app_data = {'project_name': 'Lucid AI'}
    file_path = get_session()
    with open(file_path, 'r') as f:
        text = f.read()
    cleaned_transcript = clean_up_text(text)

    return render_template('/output_pages/transcript.html', output=cleaned_transcript, app_data=app_data)

@app.route('/summary')
def summary():
    file_path = get_session()
    with open(file_path, 'r') as f:
        text = f.read()
    summarized_transcript = text_to_notes(text)

    return render_template('/output_pages/summary.html', output=summarized_transcript, app_data=app_data)

@app.route('/translate')
def translate2():
    preferred_language = request.args.get('parameter')
    file_path = get_session()
    with open(file_path, 'r') as f:
        text = f.read()
    translated_transcript = translate(text, preferred_language)

    return render_template('/output_pages/translate.html', output=translated_transcript, app_data=app_data)

@app.route('/accent')
def accent():
    preferred_accent = request.args.get('parameter')

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    CHUNK_SIZE = 1024
    if preferred_accent == "female-american":
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    elif preferred_accent == "male-american":
        url = "https://api.elevenlabs.io/v1/text-to-speech/29vD33N1CtxCmqQRPOHJ"
    elif preferred_accent == "female-british":
        url = "https://api.elevenlabs.io/v1/text-to-speech/ThT5KcBeYPX3keUQqHPh"
    elif preferred_accent == "male-british":
        url = "https://api.elevenlabs.io/v1/text-to-speech/Yko7PKHZNXotIFUBG7I9"

    file_path = get_session()
    with open(file_path, 'r') as f:
        text_to_read = f.read()

    data = {
        "text": text_to_read,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    output_file_path = os.path.join('static', 'output.mp3')

    with open(output_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    return render_template('/output_pages/accent.html', mp3_file_path="output.mp3", app_data=app_data)

@app.route('/flashcards')
def flashcards():
    file_path = get_session()
    with open(file_path, 'r') as f:
        text = f.read()
    full, keyword, description = find_keywords(text)
    return render_template('/output_pages/flashcards.html', keyword=keyword, description=description, app_data=app_data)

if __name__ == "__main__":
    app.run(debug=True)