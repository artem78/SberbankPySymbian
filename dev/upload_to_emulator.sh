#!/bin/bash

#rsync -v sberbank.py ssh://user@192.168.1.106:/s60_3rd_fp2_c/Data/python/sberbank.py
#scp sberbank.py user@192.168.1.106:/s60_3rd_fp2_c/Data/python/
sftp -b commands.sftp user@192.168.1.106
