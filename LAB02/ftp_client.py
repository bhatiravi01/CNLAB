# ftp_client.py
from ftplib import FTP

def main():
    try:
        # Connect with a 60-second timeout
        ftp = FTP(timeout=60)
        ftp.connect("test.rebex.net", 21)
        ftp.login("demo", "password")
        ftp.set_pasv(True)  # passive mode
        print("Connected to FTP server.")

        # List directory
        print("\nDirectory listing:")
        ftp.retrlines("LIST")

        # Download file
        with open("readme.txt", "wb") as f:
            ftp.retrbinary("RETR readme.txt", f.write)
        print("\nDownloaded 'readme.txt'.")

        # Upload a test file (demo server may not allow it)
        with open("upload_test.txt", "w") as f:
            f.write("Hello FTP upload from Python.")

        try:
            with open("upload_test.txt", "rb") as f:
                ftp.storbinary("STOR upload_test.txt", f)
            print("Uploaded 'upload_test.txt'.")
        except Exception as e:
            print(f"Upload failed: {e}")
            print("Note: Demo server may not allow uploads.")

        # Close the connection
        ftp.quit()
        print("\nFTP session closed.")

    except Exception as e:
        print(f"FTP failed: {e}")

if __name__ == "__main__":
    main()
