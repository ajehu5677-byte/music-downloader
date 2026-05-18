import io
import os
import json
import urllib.request
import urllib.parse
import subprocess
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

def global_unblocked_api_search(query):
    """Fetches global music search results via stable, unblocked open music directory databases."""
    encoded_query = urllib.parse.quote(query)
    
    # Secure, stable worldwide open music database API mirror
    url = f"https://saavn.dev{encoded_query}"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        results = []
        # Parse data structure from the global music network response arrays
        items = data.get('data', {}).get('results', []) if isinstance(data, dict) else []
        
        if not items:
            return None
            
        for item in items:
            track_name = item.get('name', 'Unknown Track')
            artists = item.get('artists', {}).get('primary', [])
            artist_name = artists[0].get('name', 'Various Artists') if artists else 'Unknown Artist'
            full_title = f"{artist_name} - {track_name}"
            
            # Map dynamic download request pipelines via keyword matching query lookups
            download_query_string = f"{full_title} official audio"
            
            # Extract image preview files cleanly
            image_list = item.get('image', [])
            thumb_url = image_list[-1].get('url') if image_list else "https://unsplash.com"
            
            results.append({
                "id": item.get('id', 'track'),
                "title": full_title,
                "video_url": f"ytsearch:{download_query_string}", # Safely directs yt-dlp to search and grab the audio track stream automatically
                "thumbnail": thumb_url
            })
            
            if len(results) >= 5:
                break
                
        return results if results else None
        
    except Exception as e:
        print(f"Global Directory API Mirror warning: {str(e)}")
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
