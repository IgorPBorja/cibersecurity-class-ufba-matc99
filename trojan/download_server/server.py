import argparse
from pathlib import Path

from flask import Flask, send_file


app = Flask(__name__)

TARGET_FILE = Path("binary.bin")


@app.route("/")
def download_binary():
    if not TARGET_FILE.is_file():
        return {"error": "Binary not found"}, 404

    return send_file(
        TARGET_FILE,
        as_attachment=True,
        download_name=TARGET_FILE.name,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Binary Download API")
    parser.add_argument("binary_path", help="Local path to the binary to expose at /")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    TARGET_FILE = Path(args.binary_path).expanduser().resolve()
    if not TARGET_FILE.is_file():
        raise SystemExit(f"Binary not found: {TARGET_FILE}")

    app.run(host=args.host, port=args.port)
