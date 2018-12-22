#! /bin/bash
export FLASK_APP=ss.py
export FlASK_ENV=development
export FLASK_DEBUG=1
python3 -m flask run
