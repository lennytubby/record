#!/bin/bash
./requirements-ubuntu
python3 -m pip install -r ./requirements-pip.txt
nohup python3 -u ./record.py > output_recrod.log &
nohup ./checkrunning.sh record.py > output_checkrunning.log &
