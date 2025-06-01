#!/bin/bash

error_exit() {
    echo "Error: $1" >&2
    exit 1
}

if ! command -v python3 >/dev/null 2>&1; then
    error_exit "python3 is not installed. Please install Python 3 and re-run this script."
fi

VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python 3 virtual environment in ./$VENV_DIR..."
    python3 -m venv "$VENV_DIR" \
        || error_exit "Failed to create virtual environment."
else
    echo "Virtual environment already exists in ./$VENV_DIR. Skipping creation."
fi

REQ_FILE="requirements.txt"
if [ -f "$REQ_FILE" ]; then
    echo "Installing Python packages from $REQ_FILE into the virtual environment..."
    "$VENV_DIR/bin/pip" install --upgrade pip >/dev/null 2>&1
    "$VENV_DIR/bin/pip" install -r "$REQ_FILE" \
        || error_exit "Failed to install packages from $REQ_FILE."
else
    echo "Warning: $REQ_FILE not found. Skipping package installation."
fi

ENV_FILE=".env"
ENV_EXAMPLE=".env.example"

if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE" ]; then
        echo "No .env file found. Creating .env from .env.example..."
        cp "$ENV_EXAMPLE" "$ENV_FILE" \
        || error_exit "Failed to copy $ENV_EXAMPLE to $ENV_FILE."
        echo
        echo "A new .env file has been created. Please fill it out with the appropriate values, then re-run this script."
        exit 1
    else
        error_exit "$ENV_FILE and $ENV_EXAMPLE are both missing. Cannot proceed."
    fi
fi

if [ -f "$ENV_EXAMPLE" ]; then
    if cmp -s "$ENV_FILE" "$ENV_EXAMPLE"; then
        echo
        echo "The .env file is still identical to .env.example."
        echo "Please update .env with real configuration values, then re-run this script."
        exit 1
    fi
else
    echo "Warning: $ENV_EXAMPLE not found. Cannot compare .env against example."
fi

SCRIPT_DIR="$(pwd)"
PYTHON_PATH="$SCRIPT_DIR/$VENV_DIR/bin/python"
APP_PATH="$SCRIPT_DIR/main.py"

echo
echo "Setup is complete."
echo
echo "To schedule your UniFi2CiscoSync to run every 5 minutes, add the following line to your crontab:"
echo
echo "    */5 * * * * $PYTHON_PATH $APP_PATH"

