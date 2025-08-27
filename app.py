import os
import json
import replicate
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            image_bytes = self.rfile.read(content_length)

            # The replicate library automatically finds the secret key
            # from the environment variables we just set in Render.
            output = replicate.run(
                "yorickvp/llava-13b:e27215381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
                input={
                    "image": image_bytes,
                    "prompt": "Describe this image in detail."
                }
            )

            full_description = "".join(list(output))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"description": full_description}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Server function crashed: {str(e)}"}).encode('utf-8'))
        return

# This part runs the server. Render will use the PORT environment variable it provides.
port = int(os.environ.get("PORT", 8000))
server_address = ('', port)
httpd = HTTPServer(server_address, SimpleAPIHandler)
print(f"Starting server on port {port}...")
httpd.serve_forever()
