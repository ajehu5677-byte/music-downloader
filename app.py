import io
import os
import json
import urllib.request
import urllib.parse
import subprocess
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def handle_search():
    """An internal proxy route that completely bypasses browser CORS network blocking restrictions."""
    try:
        data = request.get_json() or {}
        query = data.get('query', '').strip()
        if not query:
            return jsonify({"success": False, "error": "Search string is empty"})
            
        encoded_query = urllib.parse.quote(query)
        # Hits an open, global high-fidelity music repository directory API node
        url = f"https://jamendo.com{encoded_query}"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=6) as response:
            raw_data = json.loads(response.read().decode('utf-8'))
            
        results = []
        items = raw_data.get('results', [])
        
        for item in items:
            track_name = item.get('name', 'Unknown Track')
            artist_name = item.get('artist_name', 'Various Artists')
            full_title = f"{artist_name} - {track_name}"
            
            results.append({
                "id": item.get('id', 'track'),
                "title": full_title,
                "video_url": f"ytsearch:{fullTitle} official audio"
            })
            
        return jsonify({"success": True, "results": results})
        
    except Exception as e:
        print(f"Internal routing block check notice: {str(e)}")
        return jsonify({"success": False, "error": "Search mirror is currently busy. Please retry."})

@app.route('/download_proxy')
def download_proxy():
    """Streams audio data dynamically through Render pipelines via yt-dlp."""
    url = request.args.get('url')
    title = request.args.get('title', 'music_track')
    if not url:
        return "Missing tracking parameters.", 400
        
    try:
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip()
        filename = f"{safe_title}.mp3"
        
        command = [
            'yt-dlp', 
            '-x', 
            '--audio-format', 'mp3', 
            '--audio-quality', '0', 
            '-o', '-', 
            url
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        
        def generate_chunks():
            while True:
                chunk = process.stdout.read(4096)
                if not chunk:
                    break
                yield chunk
                
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': 'audio/mpeg'
        }
        return Response(generate_chunks(), headers=headers)
    except Exception as e:
        return f"Streaming link connection timeout: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
