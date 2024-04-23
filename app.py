import json
import os
import requests

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
        analysis = analyze_transcript(transcript)
        print("Analysis Content:", analysis)
        return render_template('index.html', transcript=transcript, analysis=analysis)
    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"Failed to fetch transcript: {e}")
        flash('Failed to fetch transcript. Please check the URL and try again.', 'error')
        return redirect(url_for('index'))

def analyze_transcript(transcript):
    url = "http://localhost:11434/api/generate"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
     # Include the transcript in the prompt
    prompt_text = f"""
        Provide an analysis and summary of the transcript, focusing on the following points?
        Key Themes: What are the primary themes discussed in the video?
        Major Insights: What significant insights or conclusions are drawn by the speaker(s)?
        Practical Implications: How do the discussions translate into practical applications or implications for the industry or topic mentioned?
        Contrasts and Comparisons: Are there any comparisons or contrasts made with other industry practices, technologies, or theoretical frameworks?
        Future Outlook: What predictions or future trends are suggested in the discussions? 
        Here is the transcript for your reference: {transcript}
    """

    data = {
        "model": "llama3",
        "prompt": prompt_text,
        "stream": False,
        "max_tokens": 4000,
        "temperature": 0.8
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        return actual_response
    else:
        print("Error: ", response.status_code, response.text)
        return "Failed to analyze transcript"

# This block ensures the server runs only if the script is executed directly
if __name__ == '__main__':
    # Configures the server to be accessible externally and run on port 5000
    app.run(host='0.0.0.0', port=5001, debug=os.getenv('FLASK_DEBUG', False))
