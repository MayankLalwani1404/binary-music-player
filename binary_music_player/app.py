from flask import Flask, render_template, send_file, jsonify
from generate_audio import generate_full_song
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate_audio():
    patterns = generate_full_song()
    print("Generated new song with patterns:", patterns)
    return jsonify({'success': True, 'timestamp': time.time()})  # timestamp helps bust caching

@app.route('/audio')
def stream_audio():
    return send_file('generated/audio.wav', mimetype='audio/wav')

if __name__ == '__main__':
    os.makedirs('generated', exist_ok=True)
    app.run(debug=True)
