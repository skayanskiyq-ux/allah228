from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "no url"}), 400

    ydl_opts = {
        "format": "mp4/best",
        "outtmpl": "video.%(ext)s",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({"file": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
