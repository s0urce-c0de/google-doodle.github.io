# How to do a full test
First, save this messy code I put together: `test_server.py`
```python
#!/usr/bin/env python3
import http.server
import socketserver
import pathlib
import os

ROOT="google-doodle.github.io"

parent_path=pathlib.Path(__file__).parent.resolve()

os.chdir(parent_path)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
  def translate_path(self, path):
    path = path.replace("#", "?").split("?")[0] # handle url params and hashes
    if any([path.startswith(f"/{i}") for i in os.listdir()]):
      path = parent_path / path[1:]
      print(path)
    else:
      path = os.path.abspath(f"{ROOT}{path}")
      print(path)
    return str(path)

PORT = 8000

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
  print("Serving at port", PORT)
  httpd.serve_forever()
```
Then run in that directory clone the doodles, do the setup, etc. (Also you need to be a coder to understand the sh\*tty mess i made.). Figure it out if you are smart.

USE:
```bash
export PORT=${PORT:-8000}
curl https://tunnel.pyjam.as/8000 > /tmp/$PORT-tunnel.conf && wg-quick up /tmp/$PORT-tunnel.conf
( trap exit SIGINT ; read -r -d '' _ </dev/tty )
wg-quick down /tmp/$PORT-tunnel.conf
rm -rf /tmp/$PORT-tunnel.conf
```
to use a fast instance.
First install the dependencies though.