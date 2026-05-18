import io
import os
import subprocess
from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/download_proxy')
def download_proxy():
    """Streams data dynamically through Render back to user via yt-dlp."""
    url = request.args.get('url')
    title = request.args.get('title', 'music_track')
    
    if not url:
        return "Missing tracking parameters.", 400
        
    try:
        # Construct clean filename string for the music download file delivery
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
