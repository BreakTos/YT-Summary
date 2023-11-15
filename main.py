from flask import Flask, request , jsonify
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def give_summary(video_id):
    
    # Get subtitles from YouTubeTranscriptApi
    subtitles = YouTubeTranscriptApi.get_transcript(video_id)

    # Extract text from the transcript
    main_content = " ".join(x["text"] + " " for x in subtitles)

    # Get video title from YouTube
    video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    main_content = video.title + " " + main_content

    print("Original Content:")
    print((len)(main_content))

    # Use GPT-3.5 for abstractive summarization
    summarizer = pipeline("summarization")
    

    x = main_content.split()
    print(len(x))
    x = x[:min(len(x), 900)]
    print(len(x))
    main_content = " ".join(x)

    summary = summarizer(main_content[:min(len(main_content),1000)], max_length=500, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
    print((len)(summary[0]["summary_text"]))
    return summary[0]["summary_text"]
    
    
        

@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'POST':
        print(request.get_json())
        data = request.get_json()
        video_id = data.get('video_id')
        
        summary = give_summary(video_id)
        print(summary)
        return summary

        return jsonify({'summary': summary})
    else:
        # HTML content with "hi" for GET requests
        html_content = "<html><body><h1>hi</h1></body></html>"
        return html_content

if __name__ == '__main__':
    app.run(debug=True)
