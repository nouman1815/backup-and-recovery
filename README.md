
# **Smart Disaster Recovery & Data Backup System Using IBM Cloud Object Storage**




## **📌 Project Overview**
The Smart Disaster Recovery & Data Backup System is designed to help small businesses securely back up and recover critical data using IBM Cloud Object Storage. This system ensures automated backups, AES-256 encryption, real-time monitoring, and disaster recovery to prevent data loss
## **Features**

- Secure Cloud Backup – Files are encrypted and stored in IBM Cloud Object Storage.

- Automated Backup Scheduling – Uses IBM Cloud Functions to automate daily backups.

- Disaster Recovery – IBM Cloud Functions enable seamless file recovery.

- User-Friendly Interface – A React.js frontend allows easy file management.

- AES-256 Encryption – Ensures data protection before upload.

- IBM Cloud Monitoring – Tracks backup success and system health.


## **📌 Explanation of Key Components**

1. **📁 Backend (Flask)**

*  app.py → Handles API requests for uploading, downloading, encrypting, and decrypting files.
*  encryption.py → Contains AES-256 encryption logic.
*  backup.py → Script that automates daily backup to IBM Cloud Object Storage.
*  .env → Stores IBM Cloud credentials securely.

2. **📁 Frontend (React)**
- App.js → Main React component with file upload, list, and download features.
- api.js → Handles Axios API requests to communicate with Flask.
- styles.css → Custom UI styling for improved aesthetics.
- .env → Stores backend API URL to keep it dynamic.
3. **📁 Cloud (IBM Cloud Functions)**
- ibm_function_backup.py → IBM Cloud Function that triggers automatic backups.
- deploy.sh → Shell script to deploy IBM Cloud Functions with one command.
4. **📁 Scripts (Helper Utilities)**
* start_backend.sh → Bash script to start Flask backend easily.
* start_frontend.sh → Bash script to start React frontend easily.
* cron_jobs.txt → Lists scheduled tasks for backup automation.

## **⚙️ Installation & Setup**

1️⃣ Clone the Repository

```bash
  git clone https://github.com/yourusername/smart-disaster-recovery.git
  cd smart-disaster-recovery
```
2️⃣ Backend Setup (Flask API)
```bash
  cd backend
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  pip install -r requirements.txt
```
Configure IBM Cloud Credentials in .env:
```bash
  COS_ENDPOINT=https://s3.us.cloud-object-storage.appdomain.cloud
  COS_API_KEY_ID=your-api-key
  COS_ACCESS_KEY=your-access-key
  COS_SECRET_KEY=your-secret-key
  BUCKET_NAME=your-bucket-name
```
Run the Flask server:
```bash
  python app.py
```
3️⃣ Frontend Setup (React.js UI)
```bash
  cd ../frontend
  npm install
```
Update .env with backend URL:
```bash
  REACT_APP_BACKEND_URL=http://127.0.0.1:5000
```
Start the frontend:
```bash
  npm start
```
4️⃣ Deploy IBM Cloud Functions
```bash
  cd ../cloud
  ibmcloud login --apikey YOUR_IBM_CLOUD_API_KEY
  sh deploy.sh
```

    
## **🛠️ Usage**


Upload Files – Encrypts and stores files in IBM Cloud Object Storage.

Automated Backup – Runs daily via IBM Cloud Functions.

Recovery – Users can restore encrypted files from the cloud.

## **🛡️ Security Measures**

✅ AES-256 encryption before storing files.

✅ Role-based access control prevents unauthorized access.

✅ IBM Key Protect for secure encryption key management.

✅ IBM Cloud Object Lock to prevent accidental deletion.

## **📊 Monitoring & Logging**

📌 IBM Cloud Monitoring tracks backup status.

📌 Logging enabled for debugging failed backups.

📌 Alerts & notifications set for backup failures.

## **🛠️ Future Enhancements**

🔹 AI-based anomaly detection for backup failure prediction.

🔹 Multi-cloud support (AWS, Azure) for redundant backups.

🔹 Mobile app integration for on-the-go management.

🔹 Blockchain integration for tamper-proof backup verification.

## **🤝 Contribution**

Fork the repository.

Create a feature branch (git checkout -b feature-name).

Commit your changes (git commit -m "Added feature XYZ").

Push to GitHub (git push origin feature-name).

Open a Pull Request.

## Screenshots

https://github.com/nouman1815/backup-and-recovery/blob/main/Screenshot%202025-02-26%20225619.png

## Authors

https://github.com/nouman1815
