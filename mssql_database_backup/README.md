# MSSQL Automated Backup to Google Drive

This project automates the process of backing up MSSQL databases and uploading them to Google Drive. It also performs cleanup of old local and Drive backups based on retention policies.

## Features

- Automatically detects all user-created MSSQL databases
- Creates `.bak` file backups using `sqlcmd`
- Uploads backups to Google Drive via service account
- Retains limited local and cloud backups (based on configurable limits)
- Scheduled using `cron` or can be triggered manually
- Implemented in Python

## Requirements

- Python 3.8+
- Google Drive API credentials (Service Account)
- MSSQL with `sqlcmd` utility installed and accessible
- Internet connection for Drive uploads

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/joinmelist/Devops_Learning.git
cd mssql-drive-backup
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```txt
google-api-python-client
google-auth
google-auth-httplib2
google-auth-oauthlib
```

### 3. Enable Google Drive API & Create Service Account

- Go to https://console.developers.google.com/
- Enable the Google Drive API
- Create a Service Account
- Download the JSON credentials file and rename it to `apikeys.json`
- Share your Google Drive backup folder with the service account’s email

### 4. Configuration

Update these variables in your script:

```python
backupDir = 'D:\\Database Backup\\'  # Change to your backup folder
maxLocalBackups = 1  # Local backup retention
maxDriveBackups = 1  # Google Drive retention
driveFolderId = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'  # Target folder for uploads
```

Also ensure the correct path to sqlcmd:

```python
sqlcmd_path = r"C:\\Path\\To\\sqlcmd.exe"
```

### 5. Run the Script Manually

```bash
python backup_script.py
```

This script will:

- List user databases
- Create a timestamped `.bak` backup for each
- Upload them to Drive
- Delete older backups exceeding the configured limits

### 6. Schedule Automatic Backups (Optional)

Use cron (Linux) or Task Scheduler (Windows) to schedule `python backup_script.py` daily or weekly.

Example cron job (Linux):

```bash
0 6 * * * /usr/bin/python3 /path/to/backup_script.py >> /var/log/mssql_backup.log 2>&1
```

Or, for Windows Task Scheduler, point to your Python executable and script.

---

## Troubleshooting

- `'sqlcmd' not found`: Ensure SQLCMD is installed and in your system PATH.
- `Google API permission denied`: Make sure the service account has access to the Drive folder.
- Backup not created: Check SQL Server permissions and disk space.
