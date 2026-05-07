import argparse
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse


app = FastAPI(title="Binary Download API")

TARGET_FILE = Path("binary.bin")


@app.get("/")
async def download_binary() -> FileResponse:
	if not TARGET_FILE.is_file():
		raise HTTPException(status_code=404, detail="Binary not found")

	return FileResponse(path=TARGET_FILE, filename=TARGET_FILE.name, media_type="application/octet-stream")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Binary Download API")
	parser.add_argument("binary_path", help="Local path to the binary to expose at /")
	parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
	parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	TARGET_FILE = Path(args.binary_path).expanduser().resolve()
	if not TARGET_FILE.is_file():
		raise SystemExit(f"Binary not found: {TARGET_FILE}")

	uvicorn.run(app, host=args.host, port=args.port)
