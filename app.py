from flask import Flask, render_template, request, jsonify, Response
import yt_dlp
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_music():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Please enter a search term'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch10',
        'extractor_args': {'youtube': {'player_client': ['web_safari']}},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            results = []
            
            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        duration_sec = entry.get('duration') or 0
                        minutes = duration_sec // 60
                        seconds = duration_sec % 60
                        formatted_duration = f"{minutes}:{seconds:02d}"

                        # Predict file sizes based on duration metrics
                        sizes = {
                            '320': round((320 * duration_sec) / 8 / 1024, 2),
                            '256': round((256 * duration_sec) / 8 / 1024, 2),
                            '192': round((192 * duration_sec) / 8 / 1024, 2),
                            '128': round((128 * duration_sec) / 8 / 1024, 2),
                            '64':  round((64 * duration_sec) / 8 / 1024, 2)
                        }

                        results.append({
                            'id': entry.get('id'), # This extracts the vital unique video identification string
                            'title': entry.get('title'),
                            'download_url': entry.get('url'),
                            'thumbnail': entry.get('thumbnail') or 'https://placeholder.com',
                            'channel': entry.get('uploader') or 'Unknown Channel',
                            'duration': formatted_duration,
                            'sizes': sizes
                        })
            
            return jsonify({'results': results, 'query': query})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_proxy')
def download_proxy():
    url = request.args.get('url')
    title = request.args.get('title', 'music_track')
    if not url:
        return "Missing stream parameter.", 400
        
    try:
        req = requests.get(url, stream=True)
        headers = {
            'Content-Disposition': f'attachment; filename="{title}.mp3"',
            'Content-Type': 'audio/mpeg'
        }
        return Response(req.iter_content(chunk_size=1024*1024), headers=headers)
    except Exception as e:
        return f"Download failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
