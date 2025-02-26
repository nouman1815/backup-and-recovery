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
RECOVERY_FOLDER = "recovered_files"

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
    IBM Cloud Function: Recovers files from IBM Cloud Object Storage.
    """
    if "filename" not in params:
        return {"error": "Filename required for recovery"}

    filename = params["filename"]
    encrypted_filename = f"{filename}.enc"
    file_path = os.path.join(RECOVERY_FOLDER, filename)

    try:
        # Download encrypted file
        response = cos_client.get_object(Bucket=BUCKET_NAME, Key=encrypted_filename)
        encrypted_data = response["Body"].read()

        # Decrypt data
        decrypted_data = cipher.decrypt(encrypted_data)

        # Save decrypted file
        os.makedirs(RECOVERY_FOLDER, exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)

        return {"message": f"File {filename} recovered successfully!"}

    except Exception as e:
        return {"error": str(e)}
