from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

def search_youtube_ytdlp(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': False, # Set to False so it gathers complete video metadata strings
        'skip_download': True,
        'allowed_extractors': ['youtube', 'youtube:search'],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' not in info or not info['entries']:
                return []
            
            results = []
            for entry in info['entries']:
                if not entry:
                    continue
                v_id = entry.get('id')
                v_title = entry.get('title', 'Unknown Track')
                
                results.append({
                    "id": v_id,
                    "title": v_title,
                    "embed_url": f"https://youtube.com{v_id}",
                    "thumbnail": f"https://youtube.com{v_id}/mqdefault.jpg"
                })
            return results
    except Exception as e:
        print(f"yt-dlp search error: {e}")
        return []


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def handle_search():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty"})
        
    search_results = search_youtube_ytdlp(query)
    if search_results:
        # Send the top result directly to your step layout panels
        return jsonify({"success": True, "results": search_results[0]})
    else:
        return jsonify({"success": False, "error": "No matching streams found."})

if __name__ == '__main__':
    # Binds directly to Render's required host environment port
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
