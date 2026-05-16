from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download/<video_id>')
def download_page(video_id):
    title = request.args.get('title', 'Unknown Track')
    return render_template('download.html', video_id=video_id, title=title)

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
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            yt_search = ydl.extract_info(f"ytsearch5:{query}", download=False)
            if 'entries' in yt_search:
                for entry in yt_search['entries']:
                    v_id = entry.get('id')
                    if v_id:
                        results.append({
                            "id": v_id,
                            "title": entry.get('title'),
                            "duration": entry.get('duration_string', 'N/A'),
                            "channel": entry.get('uploader', 'Unknown Artist'),
                            "source": "YouTube"
                        })
    except Exception as e:
        print(f"Search engine error: {e}")

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
