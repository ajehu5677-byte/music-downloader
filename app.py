from flask import Flask, request, jsonify, render_template
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    # This serves your HTML homepage
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_music():
    query = request.form.get('query')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    # Configure yt_dlp to search globally across YouTube and SoundCloud
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True,  # Fast extraction without downloading
    }

    results = []
    
    # 1. Search YouTube (returns top 3 global results)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            yt_search = ydl.extract_info(f"ytsearch3:{query}", download=False)
            if 'entries' in yt_search:
                for entry in yt_search['entries']:
                                        results.append({
                        "title": entry.get('title'),
                        "source": "YouTube",
                        "url": f"https://youtube.com{entry.get('id')}"
                    })

    except Exception as e:
        print(f"YouTube search error: {e}")

    # 2. Search SoundCloud (returns top 2 global results)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            sc_search = ydl.extract_info(f"scsearch2:{query}", download=False)
            if 'entries' in sc_search:
                for entry in sc_search['entries']:
                    results.append({
                        "title": entry.get('title'),
                        "source": "SoundCloud",
                        "url": entry.get('url')
                    })
    except Exception as e:
        print(f"SoundCloud search error: {e}")

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
