import csv
import subprocess
import os
import config
import paramiko

#VARIABLES
VM_USERNAME = 'hughj095'          
VM_IP = '172.191.171.163'       
REMOTE_DIRECTORY = 'data/'  
LOCAL_FILE_PATH = 'data.csv'

# Data you want to save as CSV
data = [
    ['Name', 'Age', 'City'],
    ['John', 30, 'New York'],
    ['Jane', 25, 'Los Angeles'],
    ['Alice', 28, 'Chicago']
]
# Writing data to CSV
with open(LOCAL_FILE_PATH, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV file saved locally as {LOCAL_FILE_PATH}")



# Construct the SCP command
#scp_command = f"sshpass -p '{config.VM_PASSWORD}' scp {local_file_path} {vm_username}@{vm_ip}:{remote_directory}"
# Run the SCP command using subprocess
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown keys
    ssh.connect(VM_IP, port=config.PORT, username=VM_USERNAME, password=config.VM_PASSWORD)
    sftp = ssh.open_sftp()
    sftp.put(LOCAL_FILE_PATH, REMOTE_DIRECTORY+LOCAL_FILE_PATH)
    sftp.close()
    print(f"File successfully uploaded to {VM_USERNAME}@{VM_IP}:{REMOTE_DIRECTORY}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred during file transfer: {e}")
