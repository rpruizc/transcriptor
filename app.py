from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_transcript():
    url = request.form['url']
    video_id = url.split('v=')[1]
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        transcript = formatter.format_transcript(transcript_list)
        return render_template('index.html', transcript=transcript)
    except Exception as e:
        return render_template('index.html', transcript=f"<p class='error-message'>An error occurred: {str(e)}</p>")

if __name__ == '__main__':
    app.run(debug=True)
