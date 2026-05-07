import argparse
import hashlib
from pathlib import Path

from flask import Flask, request, jsonify


app = Flask(__name__)

BASE_DIR = Path("uploads")


@app.route("/v1/upload", methods=["POST"])
def upload_file():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    contents = file.read()
    file_hash = hashlib.sha256(contents).hexdigest()
    safe_name = Path(file.filename).name
    destination = BASE_DIR / f"{safe_name}_{file_hash}"
    destination.write_bytes(contents)

    return jsonify({
        "filename": safe_name,
        "saved_as": destination.name,
        "content_type": file.content_type or "application/octet-stream",
        "size": len(contents),
    })


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple File Upload API")
    parser.add_argument(
        "base_directory",
        help="Base directory where uploaded files will be stored",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5001, help="Port to bind to")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    BASE_DIR = Path(args.base_directory).expanduser().resolve()
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    app.run(host=args.host, port=args.port)
