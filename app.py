import os
from flask import Flask, request, render_template, redirect, url_for, flash
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# It's a good practice to keep secret keys outside the source code.
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'jhagsdJGS&khasdjhkGSD')

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_transcript():
    """Fetch and display the YouTube video transcript."""
    url = request.form.get('url')
    if not url:
        flash('URL is required.', 'error')
        return redirect(url_for('index'))

    video_id = url.split('v=')[1]
    try:
        # Fetch the transcript using the YouTubeTranscriptApi
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        transcript = formatter.format_transcript(transcript_list)
        return render_template('index.html', transcript=transcript)
    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"Failed to fetch transcript: {e}")
        flash('Failed to fetch transcript. Please check the URL and try again.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False))