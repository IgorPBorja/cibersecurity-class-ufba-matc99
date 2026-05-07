import argparse
import os

from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/execute", methods=["POST"])
def execute_command():
    data = request.get_json()
    
    if not data or "command" not in data:
        return jsonify({"error": "No command provided"}), 400
    
    command = data["command"]
    
    try:
        exit_code = os.system(command)
        return jsonify({
            "command": command,
            "exit_code": exit_code,
            "status": "executed",
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "command": command,
        }), 500


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Command Execution API")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=443, help="Port to bind to")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app.run(host=args.host, port=args.port)
