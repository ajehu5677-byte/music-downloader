import io
import os
import json
import urllib.request
import urllib.parse
import subprocess
import re
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

def unblocked_global_search(query):
    """Fetches global search results by parsing YouTube's internal layout data structure."""
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://youtube.com{encoded_query}"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        
        with urllib.request.urlopen(req, timeout=7) as response:
            html = response.read().decode('utf-8')
            
        # Extract the hidden structural data JSON payload from YouTube's page response
        json_search = re.search(r'ytInitialData\s*=\s*({.+?});', html)
        if not json_search:
            return None
            
        data = json.loads(json_search.group(1))
        
        # Navigate through YouTube's nested dictionary layout layers safely
        contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
        video_items = contents[0]['itemSectionRenderer']['contents']
        
        results = []
        for item in video_items:
            if 'videoRenderer' not in item:
                continue
                
            video_data = item['videoRenderer']
            v_id = video_data.get('videoId')
            if not v_id:
                continue
                
            # Safely parse text objects out of the nested titles dictionary array
            title_text = "Unknown Track"
            if 'title' in video_data and 'runs' in video_data['title']:
                title_text = video_data['title']['runs'][0].get('text', 'Unknown Track')
                
            results.append({
                "id": v_id,
                "title": title_text,
                "video_url": f"https://youtube.com{v_id}",
                "thumbnail": f"https://youtube.com{v_id}/mqdefault.jpg"
            })
            
            # Limit our dashboard feed to exactly 5 search cards
            if len(results) >= 5:
                break
                
        return results if results else None
        
    except Exception as e:
        print(f"Backend processor extraction exception: {str(e)}")
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
        
    search_result = unblocked_global_search(query)
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
