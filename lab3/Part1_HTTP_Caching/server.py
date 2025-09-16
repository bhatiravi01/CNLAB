#!/usr/bin/env python3
"""
CN Lab Assignment 3 - Part 1: HTTP Caching with ETag and Last-Modified
This server implements HTTP caching using both strong (ETag) and weak (Last-Modified) validators.
"""

import http.server
import socketserver
import os
import hashlib
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime, formatdate

# Server configuration
PORT = 8080
HTML_FILE = "index.html"

class CachingHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP request handler with caching support"""
    
    def do_GET(self):
        """Handle GET requests with caching logic"""
        
        # Only serve the index.html file
        if self.path != "/" and self.path != "/index.html":
            self.send_error(404, "File not found")
            return
        
        try:
            # Read the HTML file
            with open(HTML_FILE, 'rb') as file:
                content = file.read()
            
            # Get file modification time
            file_stats = os.stat(HTML_FILE)
            last_modified_timestamp = file_stats.st_mtime
            last_modified_str = formatdate(last_modified_timestamp, usegmt=True)
            
            # Generate ETag (MD5 hash of content)
            etag = self.generate_etag(content)
            
            # Check client's cache validators
            client_etag = self.headers.get('If-None-Match')
            client_modified_since = self.headers.get('If-Modified-Since')
            
            # Print request details for debugging
            print(f"\n{'='*60}")
            print(f"Request received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Client IP: {self.client_address[0]}")
            print(f"Client ETag: {client_etag}")
            print(f"Client If-Modified-Since: {client_modified_since}")
            print(f"Server ETag: {etag}")
            print(f"Server Last-Modified: {last_modified_str}")
            
            # Check if content is cached and still valid
            is_cached = self.is_cached_content_valid(
                client_etag, 
                etag, 
                client_modified_since, 
                last_modified_timestamp
            )
            
            if is_cached:
                # Content hasn't changed - send 304 Not Modified
                print("✓ Cache is valid - sending 304 Not Modified")
                self.send_response(304)
                self.send_header('ETag', etag)
                self.send_header('Last-Modified', last_modified_str)
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.end_headers()
            else:
                # Content has changed or first request - send full content
                print("✗ Cache invalid or first request - sending 200 OK with content")
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.send_header('ETag', etag)
                self.send_header('Last-Modified', last_modified_str)
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.end_headers()
                self.wfile.write(content)
                print(f"Sent {len(content)} bytes to client")
            
            print(f"{'='*60}\n")
            
        except FileNotFoundError:
            self.send_error(404, f"File {HTML_FILE} not found")
        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500, "Internal server error")
    
    def generate_etag(self, content):
        """Generate ETag using MD5 hash of content"""
        md5_hash = hashlib.md5(content).hexdigest()
        return f'"{md5_hash}"'
    
    def is_cached_content_valid(self, client_etag, server_etag, client_modified_since, server_modified_time):
        """
        Check if cached content is still valid
        Returns True if content hasn't changed (should send 304)
        """
        
        # Check ETag (strong validator)
        if client_etag and client_etag == server_etag:
            print("  → ETag match: Content unchanged")
            return True
        
        # Check Last-Modified (weak validator)
        if client_modified_since:
            try:
                client_time = parsedate_to_datetime(client_modified_since).timestamp()
                # Allow 1 second tolerance for filesystem timestamp precision
                if server_modified_time <= client_time:
                    print("  → Last-Modified check: Content not modified since client's version")
                    return True
            except (TypeError, ValueError) as e:
                print(f"  → Error parsing client's If-Modified-Since header: {e}")
        
        return False
    
    def log_message(self, format, *args):
        """Custom log message format"""
        return  # Suppress default logging to keep console clean

def main():
    """Main function to start the server"""
    
    # Check if HTML file exists
    if not os.path.exists(HTML_FILE):
        print(f"Error: {HTML_FILE} not found!")
        print(f"Please create {HTML_FILE} in the same directory as this script.")
        return
    
    # Create and start the server
    with socketserver.TCPServer(("", PORT), CachingHTTPRequestHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"  HTTP Caching Server - CN Lab Assignment 3 Part 1")
        print(f"{'='*60}")
        print(f"Server started at http://localhost:{PORT}")
        print(f"Serving file: {HTML_FILE}")
        print(f"\nCaching features enabled:")
        print(f"  ✓ ETag (strong validator)")
        print(f"  ✓ Last-Modified (weak validator)")
        print(f"  ✓ Cache-Control headers")
        print(f"\nPress Ctrl+C to stop the server")
        print(f"{'='*60}\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped by user")
            print(f"{'='*60}\n")

if __name__ == "__main__":
    main()