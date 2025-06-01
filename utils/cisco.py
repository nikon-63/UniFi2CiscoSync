import time
import paramiko
from dotenv import load_dotenv
import os
import re

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

def cisco_fetch_networkconf():
    command = "sh vlan"
    output = connect_to_cisco_switch(command)
    if "Invalid input" in output:
        raise Exception("ERROR: Invalid command or insufficient permissions.")
    networks = []
    lines = output.splitlines()
    parsing = False
    for line in lines[2:]:
        if re.match(r"^VLAN\s+Name\s+Status\s+Ports", line):
            parsing = True
            continue
        if not parsing:
            continue
        if len(line.strip()) == 0 or re.match(r"^VLAN\s+Type\s+SAID", line):
            break
        if re.match(r"^-+", line):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        vlan_id = parts[0]
        name = parts[1]
        status = parts[2]
        ports = " ".join(parts[3:]) if len(parts) > 3 else ""
        if vlan_id in {"1", "1002", "1003", "1004", "1005"}:
            continue
        if vlan_id.isdigit():
            networks.append({
                "vlan": vlan_id,
                "name": name,
                "status": status,
                "ports": ports
            })
    return {"data": networks}

def cisco_make_network(vlan_id, vlan_name):
    command = (
        "configure terminal\n"
        f"vlan {vlan_id}\n"
        f"name {vlan_name}\n"
        "end"
    )
    output = connect_to_cisco_switch(command)

def cisco_delete_network(vlan_id):
    command = (
        "configure terminal\n"
        f"no vlan {vlan_id}\n"
        "end"
    )
    output = connect_to_cisco_switch(command)
