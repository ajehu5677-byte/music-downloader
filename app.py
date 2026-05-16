from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import os

app = Flask(__name__)

def universal_youtube_search(query):
    """Uses a public search endpoint to bypass cloud network blocks globally."""
    try:
        # Encode the search string safely for URLs
        encoded_query = urllib.parse.quote(query)
        # Using a reliable, unblocked open-source Invidious API instance for global video fetching
        url = f"https://puffyan.us{encoded_query}&type=video"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=7) as response:
            data = json.loads(response.read().decode())
            
        if not data:
            return []
            
        results = []
        # Parse out the top 3 global results matching the criteria
        for item in data[:3]:
            v_id = item.get('videoId')
            if not v_id:
                continue
                
            results.append({
                "id": v_id,
                "title": item.get('title', 'Unknown Track'),
                "embed_url": f"https://youtube.com{v_id}",
                "thumbnail": f"https://youtube.com{v_id}/mqdefault.jpg"
            })
        return results
    except Exception as e:
        print(f"Global proxy search fallback error: {e}")
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
        
    search_results = universal_youtube_search(query)
    if search_results:
        return jsonify({"success": True, "results": search_results})
    else:
        return jsonify({"success": False, "error": "Global servers are busy. Please try clicking search again."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
