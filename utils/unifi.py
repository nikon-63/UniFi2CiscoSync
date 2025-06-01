import sys
import ssl
import json
import os
from urllib.request import (
    Request,
    build_opener,
    HTTPCookieProcessor,
    HTTPSHandler,
)
from http.cookiejar import CookieJar
from dotenv import load_dotenv

# Loading environment variables from .env file
# TODO: Change so that python-dotenv is not required for this script to run
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)
CONTROLLER = os.getenv("CONTROLLER")
SITE = os.getenv("SITE")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Lets the script run without SSL verification
ssl_context = ssl._create_unverified_context()

# Stores the cookies
cookie_jar = CookieJar()
https_handler = HTTPSHandler(context=ssl_context)
opener = build_opener(https_handler, HTTPCookieProcessor(cookie_jar))

# Function that logs into the UniFi controller and stores the session cookies
def unifi_login():
    login_url = f"{CONTROLLER}/api/login"
    payload = json.dumps({"username": USERNAME, "password": PASSWORD}).encode("utf-8")
    req = Request(login_url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        resp = opener.open(req)
    except Exception as e:
        sys.exit(f"ERROR: Could not connect to {login_url}: {e}")
    status = resp.getcode()
    if status != 200:
        sys.exit(f"ERROR: Login failed (HTTP {status}).")

# Function that fetches the network configuration from the UniFi controller
def unifi_fetch_networkconf():
    url = f"{CONTROLLER}/api/s/{SITE}/rest/networkconf"
    req = Request(url, method="GET")
    try:
        resp = opener.open(req)
    except Exception as e:
        sys.exit(f"ERROR: Could not fetch {url}: {e}")
    status = resp.getcode()
    if status != 200:
        sys.exit(f"ERROR: Failed to fetch networks (HTTP {status}).")
    raw = resp.read().decode("utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: Invalid JSON received: {e}")