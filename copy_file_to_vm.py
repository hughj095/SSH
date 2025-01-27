import paramiko
import config

# Variables
HOSTNAME = '20.51.230.81'
PORT = config.PORT
USERNAME = "hughj095"
PASSWORD = config.VM_PASSWORD
LOCAL_FILE_PATH = r"C:\Users\johnm\OneDrive\Desktop\Portfolio\style.css"
REMOTE_FILE_PATH = "Portfolio/style.css"

#Functions
try:
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connect to the VM
    ssh.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
    
    # Open an SFTP session
    sftp = ssh.open_sftp()
    
    # Transfer the file
    sftp.put(LOCAL_FILE_PATH, REMOTE_FILE_PATH)
    print(f"File successfully uploaded to {REMOTE_FILE_PATH}")
    
    # Close the SFTP session and SSH connection
    sftp.close()
    ssh.close()
except Exception as e:
    print(f"An error occurred: {e}")
