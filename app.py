from api.describe import handler

# This makes the server runnable for Render
if __name__ == "__main__":
    from http.server import HTTPServer
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler)
    print("Starting server...")
    httpd.serve_forever()