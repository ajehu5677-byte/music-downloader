from flask import Flask, render_template, request, jsonify, Response
import yt_dlp
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_music():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Please enter a search term'}), 400

    # Primary Strategy: Attempt YouTube Search
    yt_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch10',
        'extractor_args': {'youtube': {'player_client': ['web_safari']}},
    }

    try:
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            results = []
            
            if 'entries' in info and len(info['entries']) > 0:
                for entry in info['entries']:
                    if entry:
                        duration_sec = entry.get('duration') or 0
                        results.append(parse_track(entry, duration_sec, 'YouTube', entry.get('id')))
                return jsonify({'results': results, 'query': query, 'source': 'YouTube'})
    
    except Exception as yt_error:
        print(f"YouTube block detected: {str(yt_error)}. Falling back to SoundCloud...")

    # Secondary Strategy: Fallback to SoundCloud if YouTube is blocked
    sc_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'scsearch10',
    }

    try:
        with yt_dlp.YoutubeDL(sc_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            results = []
            
            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        duration_sec = entry.get('duration') or 0
                        results.append(parse_track(entry, duration_sec, 'SoundCloud', entry.get('id')))
                return jsonify({'results': results, 'query': query, 'source': 'SoundCloud'})
    except Exception as sc_error:
        return jsonify({'error': f"Both networks busy: {str(sc_error)}"}), 500

def parse_track(entry, duration_sec, source, video_id):
    minutes = int(duration_sec // 60)
    seconds = int(duration_sec % 60)
    
    sizes = {
        '320': round((320 * duration_sec) / 8 / 1024, 2),
        '256': round((256 * duration_sec) / 8 / 1024, 2),
        '192': round((192 * duration_sec) / 8 / 1024, 2),
        '128': round((128 * duration_sec) / 8 / 1024, 2),
        '64':  round((64 * duration_sec) / 8 / 1024, 2)
    }

    return {
        'id': video_id,
        'title': entry.get('title'),
        'download_url': entry.get('url'),
        'thumbnail': entry.get('thumbnail') or 'https://placeholder.com',
        'channel': entry.get('uploader') or f'{source} Artist',
        'duration': f"{minutes}:{seconds:02d}",
        'sizes': sizes,
        'source': source
    }

@app.route('/download_proxy')
def download_proxy():
    url = request.args.get('url')
    title = request.args.get('title', 'music_track')
    if not url:
        return "Missing link parameters.", 400
        
    try:
        req = requests.get(url, stream=True)
        return Response(req.iter_content(chunk_size=1024*1024), headers={
            'Content-Disposition': f'attachment; filename="{title}.mp3"',
            'Content-Type': 'audio/mpeg'
        })
    except Exception as e:
        return f"Download error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
