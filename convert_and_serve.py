#!/usr/bin/env python3
"""Convert master_guide.md to HTML and serve it on localhost"""

import os
import markdown
import http.server
import socketserver
import webbrowser
from pathlib import Path

def convert_markdown_to_html(md_file, html_file):
    """Convert markdown file to HTML with styling"""
    
    # Read the markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'toc', 'tables', 'fenced_code']
    )
    
    # Create a complete HTML document with styling
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real Estate Investor's Master Guide v2.0</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 2.5em;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 2em;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }}
        
        h3 {{
            color: #2980b9;
            margin-top: 25px;
            margin-bottom: 12px;
            font-size: 1.5em;
        }}
        
        h4 {{
            color: #16a085;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        a:hover {{
            color: #2980b9;
            text-decoration: underline;
        }}
        
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        tr:hover {{
            background-color: #f5f5f5;
        }}
        
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #e74c3c;
        }}
        
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 20px 0;
            color: #555;
            font-style: italic;
            background: #f9f9f9;
            padding: 15px 20px;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        
        .nav-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #3498db;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 1000;
        }}
        
        .nav-top:hover {{
            background: #2980b9;
        }}
        
        .toc {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        
        .status-badge {{
            display: inline-block;
            background: #27ae60;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 10px 5px;
        }}
        
        .update-badge {{
            background: #3498db;
        }}
        
        .version-badge {{
            background: #9b59b6;
        }}
        
        @media print {{
            .nav-top {{
                display: none;
            }}
            .container {{
                box-shadow: none;
                max-width: 100%;
            }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            h1 {{
                font-size: 2em;
            }}
            h2 {{
                font-size: 1.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
    <div class="nav-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
        ↑ Back to Top
    </div>
    <script>
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});
        
        // Show/hide back to top button
        window.addEventListener('scroll', function() {{
            const navTop = document.querySelector('.nav-top');
            if (window.pageYOffset > 300) {{
                navTop.style.display = 'block';
            }} else {{
                navTop.style.display = 'none';
            }}
        }});
    </script>
</body>
</html>"""
    
    # Write the HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ Converted {md_file} to {html_file}")
    return html_file

def serve_html(html_file, port=8000):
    """Serve HTML file on localhost"""
    
    # Change to the directory containing the HTML file
    os.chdir(os.path.dirname(html_file))
    
    # Custom handler to serve the specific HTML file
    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path == '':
                self.path = '/' + os.path.basename(html_file)
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    # Find an available port
    while port < 9000:
        try:
            with socketserver.TCPServer(("", port), MyHandler) as httpd:
                url = f"http://localhost:{port}"
                print(f"\n🚀 Server started!")
                print(f"📱 Open your browser to: {url}")
                print(f"📄 Serving: {os.path.basename(html_file)}")
                print(f"\n⚡ Press Ctrl+C to stop the server\n")
                
                # Open browser automatically
                webbrowser.open(url)
                
                # Start serving
                httpd.serve_forever()
        except OSError:
            port += 1
            continue
        break

if __name__ == "__main__":
    # File paths
    md_file = Path(__file__).parent / "master_guide.md"
    html_file = Path(__file__).parent / "master_guide.html"
    
    print("🔄 Converting Markdown to HTML...")
    convert_markdown_to_html(md_file, html_file)
    
    print(f"\n📊 File size: {html_file.stat().st_size / 1024:.2f} KB")
    
    print("\n🌐 Starting web server...")
    serve_html(html_file)
