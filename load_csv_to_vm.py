import csv
import subprocess
import os
import config
import paramiko

#VARIABLES
vm_username = 'hughj095'          
vm_ip = '172.191.171.163'       
remote_directory = 'data/'  
local_file_path = 'data.csv'

# Data you want to save as CSV
data = [
    ['Name', 'Age', 'City'],
    ['John', 30, 'New York'],
    ['Jane', 25, 'Los Angeles'],
    ['Alice', 28, 'Chicago']
]
# Writing data to CSV
with open(local_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV file saved locally as {local_file_path}")



# Construct the SCP command
#scp_command = f"sshpass -p '{config.VM_PASSWORD}' scp {local_file_path} {vm_username}@{vm_ip}:{remote_directory}"
# Run the SCP command using subprocess
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown keys
    ssh.connect(vm_ip, port=config.PORT, username=vm_username, password=config.VM_PASSWORD)
    sftp = ssh.open_sftp()
    sftp.put(local_file_path, remote_directory+local_file_path)
    sftp.close()
    print(f"File successfully uploaded to {vm_username}@{vm_ip}:{remote_directory}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred during file transfer: {e}")
