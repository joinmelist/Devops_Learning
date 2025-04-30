import os
import subprocess
import shutil
import time
from datetime import datetime
import schedule
import time as t
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- Configuration ---
backup_dir = 'C:\\backups'
max_local_backups = 1
max_drive_backups = 1
drive_folder_id = '1z4Dke4XIFbNlVUu_ON40AcD85v9a6Vs_'
service_account_file = './central-age-458312-q3-189ede101523.json'

# --- Google Drive Setup ---
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

# --- Utility Functions ---

def exec_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    # print(result)
    if result.returncode != 0:
        raise Exception(result.stderr)
    return result.stdout

# --- Google Drive Functions ---

def upload_to_drive(file_path, db_name):
    drive_service = get_drive_service()
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [drive_folder_id]
    }
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'Uploaded to Google Drive: {file_path}')
    return file.get('id')


def cleanup_drive_backups(db_name):
    drive_service = get_drive_service()
    query = f"'{drive_folder_id}' in parents and name contains '{db_name}' and trashed = false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name, createdTime)', orderBy='createdTime desc').execute()
    files = results.get('files', [])

    matching_files = [f for f in files if f['name'].startswith(db_name + '_') and f['name'].endswith('.bak')]

    if len(matching_files) > max_drive_backups:
        for file in matching_files[max_drive_backups:]:
            drive_service.files().delete(fileId=file['id']).execute()
            print(f"Deleted old Drive backup: {file['name']}")

# --- Local Backup Functions ---

def cleanup_local_backups(db_name):
    backups = [f for f in os.listdir(backup_dir) if f.startswith(db_name + '_') and f.endswith('.bak')]
    backups = sorted(backups, key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)), reverse=True)
    if len(backups) > max_local_backups:
        for old_backup in backups[max_local_backups:]:
            os.remove(os.path.join(backup_dir, old_backup))
            print(f"Deleted local backup: {old_backup}")

# --- Backup Function ---

def backup_databases():
    try:
        # List databases
        # query = (
        #     "DECLARE @sql NVARCHAR(MAX) = ''; "
        #     "SELECT @sql = @sql + 'BACKUP DATABASE [' + name + '] TO DISK=''C:\\\\backups\\\\' + name + '_' + "
        #     "REPLACE(CONVERT(VARCHAR(20), GETDATE(), 120), ':', '-') + '.bak'' WITH INIT, COMPRESSION, STATS=10;' "
        #     "FROM sys.databases WHERE name NOT IN ('master', 'model', 'msdb', 'tempdb'); "
        #     "EXEC sp_executesql @sql;"
        # )
        sqlcmd_path = r"C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\sqlcmd.exe"
        command = [
            sqlcmd_path,
            "-S", ".",  # Server
            "-E",  # Use Windows Authentication
            "-h-1",
            "-W",
            "-k1",
            "-Q",
            "SELECT name FROM sys.databases WHERE name NOT IN ('master', 'model', 'msdb', 'tempdb');" # Query,
        ]
        # command = [query]
        output = exec_command(command)
        databases = [db.strip() for db in output.splitlines() if db.strip()]
        databases = databases[:-1]
        for db in databases:
            print(f"Processing database: {db}")
            cleanup_drive_backups(db)
            cleanup_local_backups(db)

            timestamp = int(time.time())
            backup_filename = f"{db}_{timestamp}.bak"
            backup_path = os.path.join(backup_dir, backup_filename)

            # Create backup
            backup_query = f"BACKUP DATABASE [{db}] TO DISK='{backup_path}' WITH INIT, COMPRESSION, STATS=10;"
            exec_command(f"sqlcmd -S . -E -Q \"{backup_query}\"")
            print(f"Created backup: {backup_path}")

            # Upload to Drive
            upload_to_drive(backup_path, db)

        print("Backup process completed successfully.")
    except Exception as e:
        print(f"Backup process failed: {e}")

# --- Scheduler ---

def start_scheduler():
    # schedule.every().day.at("04:36").do(backup_databases)  # Set your time here
    #
    # while True:
    #     schedule.run_pending()
    #     t.sleep(60)
    backup_databases()
if __name__ == "__main__":
    start_scheduler()
