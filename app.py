import os
from flask import Flask, request, render_template, redirect, url_for, flash
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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

# This block ensures the server runs only if the script is executed directly
if __name__ == '__main__':
    # Configures the server to be accessible externally and run on port 5000
    app.run(host='0.0.0.0', port=5555, debug=os.getenv('FLASK_DEBUG', False))
