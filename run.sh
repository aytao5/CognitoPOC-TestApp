#!/bin/bash
# Activate virtual environment and run the app
cd "$(dirname "$0")"
source venv/bin/activate
python app.py
