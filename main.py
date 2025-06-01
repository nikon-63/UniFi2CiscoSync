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

def compare_networks(unifi_vlans, cisco_vlans):
    unifi_vlan_ids = set(str(vlan["vlan"]) for vlan in unifi_vlans)
    cisco_vlan_ids = set(str(vlan["vlan"]) for vlan in cisco_vlans)
    # Checking to see if there are any vlans on the UniFi that are not on the Cisco switch
    for vlan in unifi_vlans:
        vlan_id = str(vlan["vlan"])
        vlan_name = vlan["name"]
        if vlan_id not in cisco_vlan_ids:
            print(f"Adding VLAN {vlan_id} ({vlan_name}) to Cisco switch...")
            cisco_make_network(vlan_id, vlan_name)
    # Checking to see if there are any vlans on the Cisco switch that are not on the UniFi
    for vlan in cisco_vlans:
        vlan_id = str(vlan["vlan"])
        if vlan_id not in unifi_vlan_ids:
            print(f"Deleting VLAN {vlan_id} ({vlan['name']}) from Cisco switch...")
            cisco_delete_network(vlan_id)

def main():
    print("Script started.")
    unifi_networks = unifi_connect()
    vlan_networks_unifi = sorted_networks(unifi_networks)
    vlan_networks_cisco = cisco_fetch_networkconf()

    print("Printing vlan_networks_unifi:")
    print(vlan_networks_unifi)
    print("Printing vlan_networks_cisco:")
    print(vlan_networks_cisco)

    # TODO: Put this into a function with error handling
    cisco_vlan_list = [
        {"vlan": vlan["vlan"], "name": vlan["name"]}
        for vlan in vlan_networks_cisco.get("data", [])
    ]

    compare_networks(vlan_networks_unifi, cisco_vlan_list)


if __name__ == "__main__":
    main()