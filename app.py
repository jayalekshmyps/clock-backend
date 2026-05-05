from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/api/time")
def time():
    return jsonify({
        "time": datetime.utcnow().strftime("%H:%M:%S"),
        "environment": os.getenv("ENVIRONMENT", "dev")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)