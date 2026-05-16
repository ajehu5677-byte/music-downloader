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
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Searches globally to pull 10 results from the entire world
            yt_search = ydl.extract_info(f"ytsearch10:{query}", download=False)
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
