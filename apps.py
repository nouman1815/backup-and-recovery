import os
import logging
from flask import Flask, request, jsonify, send_file
import boto3
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask app initialization
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# IBM Cloud Object Storage Configuration
COS_ENDPOINT = os.getenv("COS_ENDPOINT")
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")
COS_ACCESS_KEY = os.getenv("COS_ACCESS_KEY")
COS_SECRET_KEY = os.getenv("COS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Initialize IBM Cloud Object Storage client
cos_client = boto3.client(
    "s3",
    aws_access_key_id=COS_ACCESS_KEY,
    aws_secret_access_key=COS_SECRET_KEY,
    endpoint_url=COS_ENDPOINT,
)

# Logging Configuration
logging.basicConfig(level=logging.INFO)


# 🔹 Generate or load encryption key
ENCRYPTION_KEY_FILE = "encryption.key"
if not os.path.exists(ENCRYPTION_KEY_FILE):
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, "wb") as key_file:
        key_file.write(key)
else:
    with open(ENCRYPTION_KEY_FILE, "rb") as key_file:
        key = key_file.read()

cipher = Fernet(key)


# 🔹 Upload & Encrypt File
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Encrypt file before storing
        encrypted_data = cipher.encrypt(file.read())
        encrypted_filename = f"{filename}.enc"

        with open(file_path, "wb") as enc_file:
            enc_file.write(encrypted_data)

        # Upload encrypted file to IBM Cloud Storage
        cos_client.upload_file(file_path, BUCKET_NAME, encrypted_filename)
        os.remove(file_path)  # Remove local encrypted copy

        logging.info(f"File {filename} successfully uploaded and encrypted.")
        return jsonify({"message": "File uploaded successfully", "filename": filename})

    except Exception as e:
        logging.error(f"Upload error: {e}")
        return jsonify({"error": str(e)}), 500


# 🔹 List Files in Cloud Storage
@app.route("/files", methods=["GET"])
def list_files():
    try:
        response = cos_client.list_objects_v2(Bucket=BUCKET_NAME)
        files = [obj["Key"].replace(".enc", "") for obj in response.get("Contents", [])]
        return jsonify({"files": files})

    except Exception as e:
        logging.error(f"Error listing files: {e}")
        return jsonify({"error": str(e)}), 500


# 🔹 Download & Decrypt File
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        encrypted_filename = f"{filename}.enc"
        encrypted_path = os.path.join(app.config["UPLOAD_FOLDER"], encrypted_filename)

        # Download encrypted file from IBM Cloud Storage
        cos_client.download_file(BUCKET_NAME, encrypted_filename, encrypted_path)

        # Read and decrypt the file
        with open(encrypted_path, "rb") as enc_file:
            encrypted_data = enc_file.read()

        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        with open(decrypted_path, "wb") as dec_file:
            dec_file.write(decrypted_data)

        os.remove(encrypted_path)  # Remove encrypted file after decryption
        return send_file(decrypted_path, as_attachment=True)

    except Exception as e:
        logging.error(f"Download error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
