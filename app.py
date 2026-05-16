from flask import Flask, render_template, request, jsonify, Response
from youtubesearchpython import VideosSearch
import requests
import os

app = Flask(__name__)

def worldwide_youtube_search(query):
    """Uses an advanced internal query wrapper to fetch worldwide results securely."""
    try:
        # Search for the top 5 live matching video metadata elements globally
        videos_search = VideosSearch(query, limit=5)
        result_data = videos_search.result()
        
        if not result_data or 'result' not in result_data or len(result_data['result']) == 0:
            return None
            
        results = []
        for item in result_data['result']:
            v_id = item.get('id')
            if not v_id:
                continue
                
            # Extract the best resolution image available out of the thumbnails array list
            thumbnails = item.get('thumbnails', [])
            thumb_url = thumbnails[0].get('url') if thumbnails else f"https://youtube.com{v_id}/mqdefault.jpg"
            
            results.append({
                "id": v_id,
                "title": item.get('title', 'Unknown Track'),
                "embed_url": f"https://youtube.com{v_id}",
                "thumbnail": thumb_url
            })
        return results
    except Exception as e:
        print(f"Global metadata pipeline mapping exception: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def handle_search():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty"})
        
    search_results = worldwide_youtube_search(query)
    if search_results:
        return jsonify({"success": True, "results": search_results})
    else:
        return jsonify({"success": False, "error": "Global query limit reached. Please try general keywords."})

@app.route('/download_proxy')
def download_proxy():
    """Streams data dynamically through Render back to user to bypass cross-origin browser constraints."""
    url = request.args.get('url')
    title = request.args.get('title', 'music_track')
    if not url:
        return "Missing tracking parameters.", 400
    try:
        # Construct path to a free high-performance external fallback stream converter node
        api_extraction_endpoint = f"https://vexdl.com{url}&format=mp3&bitrate=320"
        
        req = requests.get(api_extraction_endpoint, stream=True, timeout=15)
        
        headers = {
            'Content-Disposition': f'attachment; filename="{title}.mp3"',
            'Content-Type': 'audio/mpeg'
        }
        # Pull file chunks cleanly and push directly into user browser's saving pipeline automatically
        return Response(req.iter_content(chunk_size=512*1024), headers=headers)
    except Exception as e:
        return f"Streaming link connection timeout: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
