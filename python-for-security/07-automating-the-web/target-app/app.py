"""
Simple Flask target application for Module 07 — Automating the Web.
Has a hidden /internal/status endpoint referenced only in a JS comment.
"""

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

INDEX_HTML = """<!DOCTYPE html>
<html>
<head><title>Meridian Tool Catalog</title></head>
<body>
<h1>Meridian Internal Tool Catalog</h1>
<nav>
  <a href="/">Home</a> |
  <a href="/products">Products</a> |
  <a href="/about">About</a>
</nav>
<p>Welcome to the Meridian security tool catalog. Browse available tools below.</p>
<script>
// TODO: migrate admin panel to new URL
// Internal status endpoint: /internal/status
// Remove this comment before external deployment
</script>
</body>
</html>"""

PRODUCTS_HTML = """<!DOCTYPE html>
<html>
<head><title>Products — Meridian</title></head>
<body>
<h1>Available Tools</h1>
<nav><a href="/">Home</a> | <a href="/products">Products</a> | <a href="/about">About</a></nav>
<ul>
  <li><a href="/products/scanner">Port Scanner</a></li>
  <li><a href="/products/enricher">IOC Enricher</a></li>
  <li><a href="/products/reporter">Alert Reporter</a></li>
</ul>
</body>
</html>"""

ABOUT_HTML = """<!DOCTYPE html>
<html>
<head><title>About — Meridian</title></head>
<body>
<h1>About Meridian Security</h1>
<nav><a href="/">Home</a> | <a href="/products">Products</a> | <a href="/about">About</a></nav>
<p>Meridian Financial security tooling platform.</p>
<p>Contact: <a href="mailto:security@meridian.internal">security@meridian.internal</a></p>
</body>
</html>"""

PRODUCT_HTML = """<!DOCTYPE html>
<html><head><title>{name}</title></head>
<body><h1>{name}</h1><a href="/products">Back</a><p>{desc}</p></body>
</html>"""


@app.route("/")
def index():
    return INDEX_HTML


@app.route("/products")
def products():
    return PRODUCTS_HTML


@app.route("/about")
def about():
    return ABOUT_HTML


@app.route("/products/<tool>")
def product_detail(tool):
    descriptions = {
        "scanner": "Fast TCP port scanner with banner grabbing.",
        "enricher": "IOC enrichment against multiple threat-intel feeds.",
        "reporter": "Alert deduplication and rich terminal reporting.",
    }
    return PRODUCT_HTML.format(name=tool.title(), desc=descriptions.get(tool, "Tool details."))


@app.route("/internal/status")
def internal_status():
    return jsonify({"status": "ok", "version": "2.1.0", "env": "production"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
