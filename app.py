from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_music():
    query = request.form.get('query')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True,
    }

    results = []
    
    # 1. YouTube Search
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            yt_search = ydl.extract_info(f"ytsearch3:{query}", download=False)
            if 'entries' in yt_search:
                for entry in yt_search['entries']:
                    video_id = entry.get('id')
                    if video_id:
                        results.append({
                            "title": entry.get('title'),
                            "source": "YouTube",
                            "url": "https://youtube.com" + str(video_id)
                        })
    except Exception as e:
        print(f"YouTube search error: {e}")

    # 2. SoundCloud Search
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            sc_search = ydl.extract_info(f"scsearch2:{query}", download=False)
            if 'entries' in sc_search:
                for entry in sc_search['entries']:
                    track_url = entry.get('url')
                    if track_url:
                        results.append({
                            "title": entry.get('title'),
                            "source": "SoundCloud",
                            "url": str(track_url)
                        })
    except Exception as e:
        print(f"SoundCloud search error: {e}")

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
