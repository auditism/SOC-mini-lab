from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# IMPORTANT: Update this path to match your Ubuntu directory
LOG_FILE = '/home/giorgio/simulated_logs/login_events.log'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        # This handles the CORS preflight request
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        log_data = json.loads(post_data.decode('utf-8'))
        
        # Format the log entry to be a single line for Splunk
        log_entry = json.dumps(log_data)
        
        try:
            with open(LOG_FILE, 'a') as f:
                f.write(log_entry + '\n')
            
            print(f"Logged event: {log_entry}")
            self._set_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        except IOError as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({'error': f"Failed to write to log file: {e}"}).encode('utf-8'))

def run_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=5001):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server is running on http://0.0.0.0:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
