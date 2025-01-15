### Remote laptop health check with SSH and email alerts

import paramiko
import smtplib
from email.mime.text import MIMEText
import config 

#variables
SERVER = {
    "hostname": "20.84.75.9",
    "port" : 22,
    "username" : "vmJohn08",
    "password" : config.VM_PASSWORD
}
RECIPIENT = 'john.m.hughes84@outlook.com'


#functions
def connect_to_server(server):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server["hostname"],  
            server["port"], 
            server["username"], 
            server["password"])  
        print("Connected to server")
        return client
    except Exception as e:
        print(f'Error connecting to server: {e}')
        return None

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.read().decode()

def check_health(client):
    cpu_command = "top -bn1 | grep Cpu"
    disk_command = "df -h /"
    cpu_usage = float(execute_command(client, cpu_command).split()[1])
    disk_usage = int(execute_command(client, disk_command).split()[4][:-1])
    print(f'CPU Usage is {cpu_usage}%')
    print(f'Disk Usage is {disk_usage}%')
    alerts = []
    if cpu_usage > 80:
        alerts.append(f'CPU usage is {cpu_usage}%')
    if disk_usage > 80:
        alerts.append(f'Disk usage is {disk_usage}%')
    return alerts

def send_email(alerts):
    sender = config.SENDER
    recipient = RECIPIENT
    subject = "Server Health Check"
    body = "\n".join(alerts)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.sendmail(sender, recipient, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f'Error sending email: {e}')

def main():
    client = connect_to_server(SERVER)
    if client:
        alerts = check_health(client)
        if alerts:
            send_email(alerts)
        client.close()

if __name__ == "__main__":
    main()