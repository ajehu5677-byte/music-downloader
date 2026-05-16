from flask import Flask, render_template, request, jsonify
from youtubesearchpython import VideosSearch
import os

app = Flask(__name__)

def live_global_search(query):
    """Uses youtube-search-python to fetch live data without hitting blocked third-party URLs."""
    try:
        # Search for the top 3 items matching the phrase
        videos_search = VideosSearch(query, limit=3)
        result_data = videos_search.result()
        
        if not result_data or 'result' not in result_data or len(result_data['result']) == 0:
            return []
            
        results = []
        for item in result_data['result']:
            v_id = item.get('id')
            if not v_id:
                continue
                
            # Safely grab the highest quality available thumbnail image dictionary entry
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
        print(f"Internal wrapper search error: {e}")
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
        
    search_results = live_global_search(query)
    if search_results:
        return jsonify({"success": True, "results": search_results})
    else:
        return jsonify({"success": False, "error": "No matching media tracks found. Try general keywords."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
