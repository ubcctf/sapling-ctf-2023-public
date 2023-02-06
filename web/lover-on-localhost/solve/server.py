import http.server

# This must run from the solve folder
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            path = self.path[1:]
            if path.startswith('index.html'):
                path = 'index.html'
            if path == "":
                path = "index.html"
            with open(path, "rb") as f:
                self.send_response(200)
                self.send_header("Referrer-Policy", "unsafe-url")
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
        except:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
        

httpd = http.server.HTTPServer(("0.0.0.0", 10001), Handler)
print("listening...")
httpd.serve_forever()