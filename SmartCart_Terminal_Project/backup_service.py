"""
backup_service.py
Multithreading & Automated Cloud/FTP Backup Service
Demonstrates Session 10:
  - Multithreading: threading.Thread, start(), join(), current_thread(), active_count()
  - FTP client: ftplib.FTP, connect(), login(), storbinary(), pwd(), quit()
"""

import os
import ftplib
import threading
import time
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "store.db")


def upload_database_to_ftp(ftp_host: str = "ftp.example.com",
                            ftp_user: str = "anonymous",
                            ftp_pass: str = "guest@example.com") -> bool:
    """
    Demonstrates ftplib (Session 10) for automated database archival.
    Uploads SQLite database backup to a remote FTP server.
    """
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] Starting FTP database backup routine...")

    if not os.path.exists(DB_FILE):
        print(f"[{thread_name}] Database file {DB_FILE} not found.")
        return False

    backup_filename = f"store_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

    try:
        # Simulate connection if default dummy credentials
        if ftp_host == "ftp.example.com":
            time.sleep(1.2)  # Simulating network latency
            print(f"[{thread_name}] [FTP Simulation] Connected to {ftp_host}.")
            print(f"[{thread_name}] [FTP Simulation] Uploaded '{backup_filename}' successfully.")
            return True

        # Live FTP upload
        with ftplib.FTP() as ftp:
            ftp.connect(ftp_host, 21, timeout=10)
            ftp.login(ftp_user, ftp_pass)
            print(f"[{thread_name}] FTP Current Directory: {ftp.pwd()}")
            
            with open(DB_FILE, "rb") as file_handle:
                ftp.storbinary(f"STOR {backup_filename}", file_handle)
                
            ftp.quit()

        print(f"[{thread_name}] Backup '{backup_filename}' uploaded successfully to FTP.")
        return True
    except Exception as e:
        print(f"[{thread_name}] FTP Backup Notice: {e}")
        return False


def run_async_backup(ftp_host: str = "ftp.example.com"):
    """
    Executes the backup operation in a background thread so the user interface never freezes.
    Demonstrates: threading.Thread(target=...), active_count().
    """
    worker = threading.Thread(
        target=upload_database_to_ftp,
        args=(ftp_host,),
        name="BackupWorkerThread",
        daemon=True
    )
    worker.start()
    print(f"[Main Process] Dispatched background thread. Active threads count: {threading.active_count()}")
    return worker


if __name__ == "__main__":
    t = run_async_backup()
    t.join()
    print("[Main Process] Backup finished.")
