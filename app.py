from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# List of allowed domains for security
ALLOWED_DOMAINS = ['example.com', 'wikipedia.org', 'github.com']

def is_valid_url(url):
    """Check if the URL is properly formatted and belongs to allowed domains."""
    pattern = re.compile(r'^https?:\/\/(www\.)?([\w.-]+)')
    match = pattern.match(url)
    
    if match:
        domain = match.group(2)
        if domain in ALLOWED_DOMAINS:
            return True
    return False

@app.route('/proxy', methods=['GET'])
def proxy():
    url = request.args.get('url')
    
    if not url or not is_valid_url(url):
        return jsonify({'error': 'Invalid or unauthorized URL'}), 400

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        return response.text
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
