from flask import *
import os
import assemblyai as aai
from gemini import *
import requests
from dotenv import load_dotenv
import subprocess

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

@app.route('/chat_with_pdf')
def chat_with_pdf():
    subprocess.Popen(["streamlit", "run", "chat_pdf.py"])
    return redirect(url_for('index'))

@app.route('/boring_slide_eradicator')
def boring_slide_eradicator():
    subprocess.Popen(["streamlit", "run", "slide.py"])
    return redirect(url_for('index'))

@app.route('/success', methods=['POST'])
def success():
    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "Empty filename"

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    if file.filename.endswith('.mp3'):
        transcribed_text = transcribe_audio(file_path)
        transcribed_file_path = os.path.join('uploads', file.filename + ".txt")
        with open(transcribed_file_path, 'w') as f:
            f.write(transcribed_text)
        file_path = transcribed_file_path

    session['file_path'] = file_path

    output = run_python_script(file_path)
    return redirect(url_for('show_output', output=output))

def get_session():
    return session.get('file_path')

def run_python_script(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def transcribe_audio(file_path):
    config = aai.TranscriptionConfig(auto_highlights=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path, config=config)
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

    return render_template('/output_pages/translate.html', output=translated_transcript, preferred_language=preferred_language, app_data=app_data)

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
        url = "https://api.elevenlabs.io/v1/text-to-speech/pqHfZKP75CvOlQylNhV4"
    elif preferred_accent == "female-british":
        url = "https://api.elevenlabs.io/v1/text-to-speech/ThT5KcBeYPX3keUQqHPh"
    elif preferred_accent == "male-british":
        url = "https://api.elevenlabs.io/v1/text-to-speech/Yko7PKHZNXotIFUBG7I9"
    elif preferred_accent == "male-australian":
        url = "https://api.elevenlabs.io/v1/text-to-speech/zcAOhNBS3c14rBihAFp1"
    elif preferred_accent == "female-swedish":
        url = "https://api.elevenlabs.io/v1/text-to-speech/XB0fDUnXU5powFXDhCwa"
    elif preferred_accent == "male-italian":
        url = "https://api.elevenlabs.io/v1/text-to-speech/zcAOhNBS3c14rBihAFp1"

    file_path = get_session()
    if not file_path:
        return redirect(url_for('index'))

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

    return render_template('/output_pages/accent.html', mp3_file_path="output.mp3", transcript=text_to_read, app_data=app_data)

@app.route('/flashcards')
def flashcards():
    file_path = get_session()
    if not file_path:
        return redirect(url_for('index'))

    with open(file_path, 'r') as f:
        text = f.read()
        
    full, keyword, description = find_keywords(text)
    return render_template('/output_pages/flashcards.html', keyword=keyword, description=description, app_data=app_data)

@app.route('/math_solver')
def math_solver():
    subprocess.Popen(["streamlit", "run", "solver.py"])
    return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run(debug=True)
