# -*- coding: utf-8 -*-
from datetime import datetime
import os
# Για τα log files
import logging
import sys
today_obj = datetime.today()
today = datetime.today().strftime('%d/%m/%Y')  # 16/02/2023
today_str = today.replace("/", "-")
now = datetime.now()
now_str = now.strftime("%H-%M-%S")
VERSION = "V 0.0.2"
log_dir = "logs" + "/" + today.replace("/", "_") + "/"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)



log_file_name = f"{today_str}.log"
log_file = os.path.join(log_dir, log_file_name)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # or whatever

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)  # or whatever
handler = logging.FileHandler(log_file, 'a', 'utf-8')  # or whatever

handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
root_logger.addHandler(handler)
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info