#!/usr/bin/env bash

rm -rf venv3
python3 -m venv venv3
source venv3/bin/activate
pip3 install -r requirements.txt
