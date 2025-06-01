from utils.unifi import *
from utils.cisco import *

# Logic for connecting to the UniFi controller and fetching network configuration 
# using the functions defined in utils.unifi
def unifi_connect():
    print("Logging into UniFi controller...")
    try:
        unifi_login()
        print("Successfully logged into UniFi controller.")
    except Exception as e:
        sys.exit(f"ERROR: UniFi login failed: {e}")
    print("Fetching UniFi network configuration...")
    try:
        unifi_networks = unifi_fetch_networkconf()
        print("Successfully fetched UniFi network configuration.")
        return unifi_networks
    except Exception as e:
        sys.exit(f"ERROR: Could not fetch network configuration: {e}")

# Sorts the networks fetched from the UniFi controller
def sorted_networks(json_data):
    networks = json_data.get("data", [])
    if not isinstance(networks, list):
        sys.exit(f"ERROR: Invalid data format")
    result = []
    for net in networks:
        if net.get("vlan_enabled"):
            entry = {
                "name": net.get("name", "<no-name>"),
                "vlan": net.get("vlan", "<no-vlan>"),
                "subnet": net.get("ip_subnet", "<no-subnet>")
            }
            result.append(entry)
    if not result:
        sys.exit(f"ERROR: No VLAN-enabled networks found.")
    return result


def main():
    print("Script started.")
    unifi_networks = unifi_connect()
    vlan_networks = sorted_networks(unifi_networks)

    print(connect_to_cisco_switch("show version"))


if __name__ == "__main__":
    main()