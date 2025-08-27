import replicate
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            image_bytes = self.rfile.read(content_length)
            
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