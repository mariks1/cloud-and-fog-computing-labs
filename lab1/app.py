import os
from flask import Flask, render_template_string
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


HTML_TEMPLATE = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        .wrapper {
            max-width: 600px;
            margin: 80px auto;
            background: white;
            padding: 32px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            text-align: center;
        }
        h1 {
            margin-bottom: 0.5em;
        }
        .counter {
            font-size: 3rem;
            font-weight: 700;
            margin: 0.3em 0 0.8em;
        }
    </style>
</head>
<body>
<div class="wrapper">
    <h1>Мини-магазин</h1>
    <p>Счётчик посещений:</p>
    <div class="counter">{{ count }}</div>
</div>
</body>
</html>
"""


@app.route("/")
def index():
    try:
        count = redis_client.incr("hits")
        return render_template_string(HTML_TEMPLATE, count=count, error=None)
    except redis.exceptions.RedisError as e:
        return render_template_string(HTML_TEMPLATE, count=None, error=str(e))


if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", os.getenv("PORT", 5000)))
    app.run(host=host, port=port)
