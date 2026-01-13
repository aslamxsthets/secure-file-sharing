# 🔐 Secure File Sharing System

A cybersecurity-focused web application that enables **secure file upload and download** using **AES encryption**, **role-based access control**, and **audit logging**.

Built by **ASLAM JAVEED**.

---

## 🚀 Features

- 🔑 **AES-GCM Encryption**
  - Files are encrypted before storage
  - Decrypted only on authorized download

- 👤 **User Authentication**
  - Secure password hashing
  - Session-based login
  - Role-based access (User / Admin)

- 🗂️ **Per-User File Isolation**
  - Each user has a private encrypted storage directory

- 📊 **Audit Logging (MongoDB)**
  - Upload & download logs
  - Timestamp, IP address, user identity

- 🛡️ **Admin Dashboard**
  - View system activity
  - Monitor uploads & downloads
  - Access restricted to admin users

- 🎨 **Cyber-Themed UI**
  - Animated scan-line background
  - Neon accents
  - Admin badge
  - Custom branding

---

## 🏗️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** MongoDB
- **Encryption:** AES (GCM mode)
- **Frontend:** HTML, CSS (Cyber UI)
- **Auth:** Werkzeug Security
- **Logging:** MongoDB Collections

---

## 📁 Project Structure

secure_file_sharing/
│
├── app.py
├── crypto_utils.py
├── mongo_db.py
│
├── uploads/
│ └── encrypted/
│
├── static/
│ └── style.css
│
├── templates/
│  └── login.html
│  └── register.html
│  └── index.html
│  └── admin_logs.html
│  └── admin_dashboard.html

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/aslamxsthets/secure-file-sharing
cd secure-file-sharing

2️⃣ Create Virtual Environment
bash

Copy code
python -m venv venv
Activate:

Windows

bash
Copy code
venv\Scripts\activate
Linux / macOS

bash
Copy code
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy code
pip install flask pymongo pycryptodome
4️⃣ Start MongoDB
Make sure MongoDB is running locally:

bash
Copy code
mongod
5️⃣ Run the Application
bash
Copy code
python app.py
Access:

cpp
Copy code
http://127.0.0.1:5000

🔐 Admin Access
Register a normal user

Open MongoDB Compass

Edit the user document:

json
Copy code
"role": "admin"
Logout & login again

Admin URLs:
/admin/logs

/admin/dashboard

📜 Security Notes
Files are encrypted at rest using AES-GCM

Passwords are hashed (never stored in plain text)

Logs support forensic analysis

Access control enforced server-side

Designed with secure coding practices

📌 Future Enhancements
HTTPS with TLS

Dockerized deployment

Cloud hosting (Render / Railway)

AES key rotation

SIEM-style alerting

👤 Author
ASLAM JAVEED
Cybersecurity Enthusiast | Secure Systems Developer

⭐ If you like this project
Give it a ⭐ dude!!!