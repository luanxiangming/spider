import logging
import os
import sys
from config import LOG_DIR

logging.basicConfig(level=logging.DEBUG)


def create_logger_file(filename):
	try:
		base_dir = os.path.dirname(__file__)
		log_name = os.path.join(base_dir, '../', LOG_DIR, filename)
		fh = logging.FileHandler(log_name)
		fh.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
		fh.setFormatter(formatter)
		logging.getLogger().addHandler(fh)
	except:
		logging.debug(sys.exc_info())


def log(message):
	logging.debug(message)
