import argparse
import hashlib
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, UploadFile


app = FastAPI(title="Simple File Upload API")

BASE_DIR = Path("uploads")


@app.post("/v1/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str | int]:
	BASE_DIR.mkdir(parents=True, exist_ok=True)

	contents = await file.read()
	file_hash = hashlib.sha256(contents).hexdigest()
	safe_name = Path(file.filename or "upload").name
	destination = BASE_DIR / f"{safe_name}_{file_hash}"
	destination.write_bytes(contents)

	return {
		"filename": safe_name,
		"saved_as": destination.name,
		"content_type": file.content_type or "application/octet-stream",
		"size": len(contents),
	}


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Simple File Upload API")
	parser.add_argument(
		"base_directory",
		help="Base directory where uploaded files will be stored",
	)
	parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
	parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	BASE_DIR = Path(args.base_directory).expanduser().resolve()
	BASE_DIR.mkdir(parents=True, exist_ok=True)
	uvicorn.run(app, host=args.host, port=args.port)
