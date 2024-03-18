from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import hashlib
import mysql.connector
from datetime import datetime

class FileHasher(FileSystemEventHandler):
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.processed_files = set()

    def scan_directory(self):
        for root, _, files in os.walk(self.directory_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path) and file_path not in self.processed_files:
                    if file_path == "c:\\Users\\Tejaswini\\Downloads\\desktop.ini":
                        pass
                    else:
                        print()
                        print(f"Scanning file: {file_path}")
                        new_sha1, new_md5 = hash_file(file_path)
                        print("SHA-1: ",new_sha1," MD5: ", new_md5)
                        check_existing_hash(new_sha1, new_md5, file_path)
                        self.processed_files.add(file_path)

def check_existing_hash(sha1, md5, file_path):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ransomware'
        )
        cursor = connection.cursor()
        query = "SELECT * FROM signature WHERE sha1 = %s OR md5 = %s"
        cursor.execute(query, (sha1, md5))
        result = cursor.fetchone()

        if result:
            print()
            print("#############################################")
            print("Hash already exists in the database.")
            if(result[3]==1):
                print("RANSOMWARE - Proceeding to remove !!!")
                if file_path:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"{file_path} removed successfully.")
            else:
                print("GOODWARE: Safe to install")
            print("#############################################")
            print()
        else:
            print()
            print("#############################################")
            print("Hash does not exist in the database.")
            print("Proceed to Layer 2")
            print("#############################################")
            print()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    #finally:
    #    if cursor:
    #        cursor.close()
    #    if connection:
    #        connection.close()

def hash_file(file_path):
    sha1_hash = hashlib.sha1()
    md5_hash = hashlib.md5()

    
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha1_hash.update(chunk)
            md5_hash.update(chunk)
    return sha1_hash.hexdigest(), md5_hash.hexdigest()

def start_monitoring(directory_path):
    file_hasher = FileHasher(directory_path)
    while True:
        file_hasher.scan_directory()
        time.sleep(5)  

if __name__ == "__main__":
    directory_to_monitor = "c:\\Users\\Tejaswini\\Downloads"
    start_monitoring(directory_to_monitor)
    