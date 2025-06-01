from utils.unifi import *
from utils.cisco import *

def main():
    # Login to UniFi controller
    print("Logging into UniFi controller...")
    try:
        unifi_login()
        print("Successfully logged into UniFi controller.")
    except Exception as e:
        print(f"UniFi login failed: {e}")
        return
    print("Fetching UniFi network configuration...")
    try:
        unifi_networks = unifi_fetch_networkconf()
        print("Successfully fetched UniFi network configuration.")
    except Exception as e:
        print(f"Failed to fetch UniFi networks: {e}")
        return
    
    print(unifi_networks)


if __name__ == "__main__":
    main()