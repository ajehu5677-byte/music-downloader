from flask import Flask, render_template, request, Response
import yt_dlp
import requests

app = Flask(__name__)

# Function to search YouTube dynamically using yt-dlp
def search_youtube(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True,  # Fast extraction without downloading metadata
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Limits the search results to 5 videos
            info = ydl.extract_info(f"ytsearch5:{query}", download=False)
            results = []
            if 'entries' in info:
                for entry in info['entries']:
                    # Turn duration in seconds into MM:SS format
                    duration_sec = entry.get('duration', 0) or 0
                    mins = int(duration_sec // 60)
                    secs = int(duration_sec % 60)
                    duration_str = f"{mins}:{secs:02d}"

                    results.append({
                        "title": entry.get('title', 'Unknown Title'),
                        "source": "YouTube",
                        "channel": entry.get('uploader', 'Unknown Channel'),
                        "duration": duration_str,
                        "video_id": entry.get('id')
                    })
            return results
        except Exception as e:
            print(f"Search Error: {e}")
            return []

@app.route('/', methods=['GET', 'POST'])
def index():
    user_query = request.form.get('query') or request.args.get('q', '')
    results = []
    
    if user_query:
        results = search_youtube(user_query)
            
    return render_template(
        'index.html', 
        user_query=user_query, 
        results=results, 
        playing_index=None,
        active_conversion=False,
        conversion_index=None
    )

@app.route('/play/<int:index_id>')
def play_video(index_id):
    user_query = request.args.get('q', '')
    results = search_youtube(user_query) if user_query else []
    return render_template(
        'index.html',
        user_query=user_query,
        results=results,
        playing_index=index_id,
        active_conversion=False,
        conversion_index=None
    )

@app.route('/convert/<int:index_id>')
def convert_video(index_id):
    user_query = request.args.get('q', '')
    results = search_youtube(user_query) if user_query else []
    return render_template(
        'index.html',
        user_query=user_query,
        results=results,
        playing_index=None,
        active_conversion=True,
        conversion_index=index_id
    )

@app.route('/download-file')
def download_file():
    video_id = request.args.get('id')
    title = request.args.get('title', 'audio')
    
    if not video_id:
        return "Missing video ID", 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_id, download=False)
            stream_url = info.get('url')

            
            # Proxy and stream the audio data back to the browser user
            req = requests.get(stream_url, stream=True)
            
            headers = {
                'Content-Type': 'audio/mpeg',
                'Content-Disposition': f'attachment; filename="{title}.mp3"'
            }
            
            return Response(req.iter_content(chunk_size=1024*1024), headers=headers)
        except Exception as e:
            return f"Download failed: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
