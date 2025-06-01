# UniFi2CiscoSync

## Overview
**UniFi2CiscoSync** is a lightweight Python automation tool that keeps VLAN configurations synchronized between a UniFi Controller and a Cisco core switch. When you create or delete VLAN‐enabled networks in UniFi, this script will:

1. Log into the UniFi Controller and fetch the list of VLAN‐enabled networks (including VLAN IDs and their names).  
2. SSH into the Cisco switch, retrieve its current VLAN database, and then:
   - **Add** any VLANs that exist in UniFi but not on Cisco.  
   - **Remove** any VLANs that exist on Cisco but not in UniFi.  

---

## Requirements

- **Python 3.8+**  
- **Dependencies** (install via `pip install -r requirements.txt`):  
  - `python-dotenv` (for loading environment variables from `.env`)  
  - `paramiko` (SSH client library for Python)  

- **Environment variables** (see `.env.example`):  
  ```text
  # UniFi Controller
  CONTROLLER=https://<UNIFI_CONTROLLER_IP>:8443
  SITE=default
  USERNAME=<unifi_username>
  PASSWORD=<unifi_password>

  # Cisco Switch (SSH)
  SWITCH_IP=<cisco_switch_ip>
  SWITCH_USERNAME=<ssh_username>
  SWITCH_PASSWORD=<ssh_password>
  SSH_PORT=22
  ```

---

## Why Older SSH Protocols and Password Authentication?
This script uses older SSH ciphers and password-based authentication because the switch switch I have deployed is running IOS 12.2 and dose not support public-key authentication via the ip ssh pubkey-chain feature.