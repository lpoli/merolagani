import os
import shutil
import logging
from datetime import datetime

logfolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
old_logfolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'oldlogs')

if not os.path.exists(old_logfolder):
    os.mkdir(old_logfolder)
if not os.path.exists(logfolder):
    os.mkdir(logfolder)

logs = os.listdir(logfolder)
if logs:
    source_path = os.path.join(logfolder, logs[0])
    dest_path = os.path.join(old_logfolder, logs[0])
    shutil.move(source_path, dest_path)

filename = logfolder + '/' + datetime.now().strftime('mylogfile_%Y-%m-%d_%H:%M.log')
logging.basicConfig(filename=filename, filemode='w', format='%(asctime)s:%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_logger():
    return logger