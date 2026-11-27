from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to my Docker Python Application!"

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/api/info")
def info():
    return jsonify({
        "application": "Docker Flask App",
        "environment": os.getenv("APP_ENV", "development")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)