import boto3
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

# IBM Cloud Object Storage Credentials
COS_ENDPOINT = os.getenv("COS_ENDPOINT")
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Load Encryption Key
with open("encryption.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Initialize IBM Cloud Storage Client
cos_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("COS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("COS_SECRET_KEY"),
    endpoint_url=COS_ENDPOINT,
)

# Backup Folder Path
BACKUP_FOLDER = "important_files"

def backup_files():
    for filename in os.listdir(BACKUP_FOLDER):
        file_path = os.path.join(BACKUP_FOLDER, filename)

        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                encrypted_data = cipher.encrypt(file.read())

            encrypted_filename = f"{filename}.enc"

            # Save encrypted file locally before upload
            with open(encrypted_filename, "wb") as enc_file:
                enc_file.write(encrypted_data)

            # Upload encrypted file to IBM Cloud
            cos_client.upload_file(encrypted_filename, BUCKET_NAME, encrypted_filename)
            os.remove(encrypted_filename)  # Remove local copy

            print(f"Backup successful for: {filename}")

if __name__ == "__main__":
    print("Running automated backup at:", datetime.datetime.now())
    backup_files()
