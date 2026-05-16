from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import re

app = Flask(__name__)

def search_youtube(query):
    """Performs a simple YouTube search using scrape-based parsing."""
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://youtube.com{encoded_query}"
        
        # Simulating a basic browser request header
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode()
            
        # Extract video IDs and Titles using regex patterns
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        
        if not video_ids:
            return []
            
        # Clean duplicates while preserving order
        unique_ids = []
        for v_id in video_ids:
            if v_id not in unique_ids:
                unique_ids.append(v_id)
                
        # Generate clean data payload for the frontend
        results = []
        for v_id in unique_ids[:3]: # Limit to top 3 matches for reliability
            results.append({
                "id": v_id,
                "title": f"Result Track [{query.title()} Mix]",
                "embed_url": f"https://youtube.com{v_id}",
                "thumbnail": f"https://youtube.com{v_id}/mqdefault.jpg"
            })
        return results
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def handle_search():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty"})
        
    search_results = search_youtube(query)
    if search_results:
        return jsonify({"success": True, "results": search_results})
    else:
        return jsonify({"success": False, "error": "No results found or connection timeout."})

import os

if __name__ == '__main__':
    # Render requires binding to 0.0.0.0 and reading the dynamic PORT variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

