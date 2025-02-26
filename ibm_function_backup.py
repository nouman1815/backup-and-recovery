import boto3
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# IBM Cloud Object Storage credentials
COS_ENDPOINT = os.getenv("COS_ENDPOINT")
COS_API_KEY_ID = os.getenv("COS_API_KEY_ID")
COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")
COS_ACCESS_KEY = os.getenv("COS_ACCESS_KEY")
COS_SECRET_KEY = os.getenv("COS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
BACKUP_FOLDER = "backup_files"

# Encryption key loading
with open("encryption.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# IBM Cloud Object Storage client setup
cos_client = boto3.client(
    "s3",
    aws_access_key_id=COS_ACCESS_KEY,
    aws_secret_access_key=COS_SECRET_KEY,
    endpoint_url=COS_ENDPOINT,
)

def main(params):
    """
    IBM Cloud Function: Automates backup of all files in BACKUP_FOLDER to IBM Cloud Object Storage.
    """
    for filename in os.listdir(BACKUP_FOLDER):
        file_path = os.path.join(BACKUP_FOLDER, filename)
        
        if os.path.isfile(file_path):
            # Encrypt file data before upload
            with open(file_path, "rb") as file:
                encrypted_data = cipher.encrypt(file.read())

            encrypted_filename = f"{filename}.enc"
            cos_client.put_object(Bucket=BUCKET_NAME, Key=encrypted_filename, Body=encrypted_data)

            print(f"Backup successful for: {filename}")

    return {"message": "Backup process completed!"}
