from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_music():
    query = request.form.get('query')
    # ... the rest of your code stays exactly the same ...

@app.route('/search', methods=['POST'])
def search_music():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Please enter a search term'}), 400

    # Expanded configuration: pulls a wide index array from multiple public music catalogs
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'auto',  # Wider search protocol targeting open indexing channels
        'quiet': True
    }

    try:
        # We enforce a broader lookup wrapper falling back to soundcloud search if needed
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First attempt: search via wide public cloud tracks
            try:
                info = ydl.extract_info(f"scsearch15:{query}", download=False)
            except Exception:
                # Secondary wide fallback array catalog search
                info = ydl.extract_info(f"ytsearch10:{query}", download=False)
                
            results = []
            
            if info and 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        duration_sec = entry.get('duration') or 0
                        minutes = int(duration_sec // 60)
                        seconds = int(duration_sec % 60)
                        formatted_duration = f"{minutes}:{seconds:02d}"

                        sizes = {
                            '320': round((320 * duration_sec) / 8 / 1024, 2),
                            '256': round((256 * duration_sec) / 8 / 1024, 2),
                            '192': round((192 * duration_sec) / 8 / 1024, 2),
                            '128': round((128 * duration_sec) / 8 / 1024, 2),
                            '64':  round((64 * duration_sec) / 8 / 1024, 2)
                        }

                        results.append({
                            'id': entry.get('id'),
                            'title': entry.get('title'),
                            'download_url': entry.get('url'),
                            'thumbnail': entry.get('thumbnail') or 'https://placeholder.com',
                            'channel': entry.get('uploader') or 'Music Provider',
                            'duration': formatted_duration,
                            'sizes': sizes
                        })
            
            return jsonify({'results': results, 'query': query})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
