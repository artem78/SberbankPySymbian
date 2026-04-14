#!/bin/bash

#sudo apt-get install inotify-tools

while inotifywait -e close_write ../sberbank.py; do ./upload_to_emulator.sh; done
