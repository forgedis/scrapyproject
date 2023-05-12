import http.server
import socketserver

from jinja2 import Template
import psycopg2

from scrapyproject import settings

page_template = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>Scrapyproject</title>
    <style>
        ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
        }

        li {
            width: 23%;
            display: flex;
            margin-bottom: 20px;
        }

        img {
            max-width: 60%;
            margin-right: 10px;
        }

        .item-title {
            font-size: 16px;
            font-weight: bold;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
</head>
<body>
    <h1>Scraped Data</h1>
    <ul>
    {% for item in items %}
        <li>
            <img src="{{ item.image_url }}" alt="{{ item.title }}">
            <div>
                <div class="title">{{ item.title }}</div>
            </div>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
""")

class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            conn = psycopg2.connect(**settings.DATABASE)
            cur = conn.cursor()
            cur.execute('SELECT title, image_url FROM items')
            items = []
            for row in cur:
                items.append({
                    'title': row[0],
                    'image_url': row[1],
                })
            cur.close()
            conn.close()

            page = page_template.render(items=items)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(page, 'utf-8'))
        else:
            super().do_GET()

PORT = 8080
handler = HTTPHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Server started on port", PORT)
    httpd.serve_forever()