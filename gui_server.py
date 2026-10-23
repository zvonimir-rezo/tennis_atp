import http.server
import socketserver
import json
import urllib.parse
import os
import pandas as pd
from pathlib import Path

# Set up to run from the root dir so we can import predict
import sys
root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir))

from predict import run_prediction

PORT = 8000

class APIServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # API Route for getting player list
        if self.path == '/api/players':
            try:
                df = pd.read_csv(root_dir / "current_elos.csv")
                players = df.to_dict(orient="records")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(players).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return
            
        # Serve index.html at root
        if self.path == '/':
            self.path = '/gui/index.html'
            
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            try:
                p1 = data.get('p1')
                p2 = data.get('p2')
                surface = data.get('surface', 'Hard')
                odds1 = float(data.get('odds1')) if data.get('odds1') else None
                odds2 = float(data.get('odds2')) if data.get('odds2') else None
                
                result = run_prediction(p1, p2, surface, odds1, odds2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

if __name__ == "__main__":
    Handler = APIServer
    # Change directory so static files load correctly
    os.chdir(root_dir)
    with socketserver.TCPServer(("127.0.0.1", 8080), Handler) as httpd:
        print(f"Serving GUI at http://127.0.0.1:8080")
        httpd.serve_forever()
