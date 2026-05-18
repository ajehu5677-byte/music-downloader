import io
import os
import json
import urllib.request
import urllib.parse
import subprocess
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

def global_unblocked_api_search(query):
    """Fetches global music search results via public API mirror networks to completely bypass IP bans."""
    encoded_query = urllib.parse.quote(query)
    
    # List of redundant public API search mirrors to circle through automatically
    api_endpoints = [
        f"https://kavin.rocks{encoded_query}&filter=videos",
        f"https://puffyan.us{encoded_query}"
    ]
    
    for url in api_endpoints:
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            results = []
            
            # Handle standard Piped format data structure parsing
            items = data.get('content', []) if isinstance(data, dict) else data
            if not items:
                continue
                
            for item in items:
                v_id = item.get('videoId') or item.get('id')
                if not v_id:
                    continue
                    
                results.append({
                    "id": v_id,
                    "title": item.get('title', 'Unknown Track'),
                    "video_url": f"https://youtube.com{v_id}",
                    "thumbnail": f"https://youtube.com{v_id}/mqdefault.jpg"
                })
                
                if len(results) >= 5:
                    break
                    
            if results:
                return results
                
        except Exception as e:
            print(f"Mirror server node bypass warning: {str(e)}")
            continue # Try the fallback mirror automatically if one is slow or down
            
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def handle_search():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    if not query:
        return jsonify({"success": False, "error": "Input text is blank"})
        
    search_result = global_unblocked_api_search(query)
    if search_result:
        return jsonify({"success": True, "results": search_result})
    else:
        return jsonify({"success": False, "error": "Global query mirror limits hit. Please try direct keywords."})

@app.route('/download_proxy')
def download_proxy():
    """Streams data dynamically through Render back to user via yt-dlp."""
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
        
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.DEVNULL
        )
        
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
