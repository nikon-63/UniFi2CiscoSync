import time
import paramiko
from dotenv import load_dotenv
import os

# Loading environment variables from .env file
# TODO: Change so that python-dotenv is not required for this script to run
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)
SWITCH_IP = os.getenv("SWITCH_IP")
SWITCH_USERNAME = os.getenv("SWITCH_USERNAME")
SWITCH_PASSWORD = os.getenv("SWITCH_PASSWORD")
SSH_PORT = os.getenv("SSH_PORT")

def connect_to_cisco_switch(command):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    transport = paramiko.Transport((SWITCH_IP, int(SSH_PORT)))
    sec_opts  = transport.get_security_options()
    sec_opts.ciphers   = ["aes128-cbc"] + list(sec_opts.ciphers)
    sec_opts.kex       = ["diffie-hellman-group1-sha1"] + list(sec_opts.kex)
    sec_opts.key_types = ["ssh-rsa"] + list(sec_opts.key_types)
    transport.connect(username=SWITCH_USERNAME, password=SWITCH_PASSWORD)
    client._transport = transport
    channel = client.invoke_shell()
    time.sleep(0.5)
    channel.send(f"{command}\n")
    time.sleep(0.5)
    output = ""
    while channel.recv_ready():
        output += channel.recv(4096).decode("utf-8")
    channel.close()
    client.close()
    transport.close()
    transport.close()

    return output