import argparse, logging, io
from pathlib import Path
from dotenv import dotenv_values

config = dotenv_values(".env")
log_file = io.open(str(Path.home()) + config.get('LOG_DIRECTORY'), mode='a+', encoding='utf-8')
logging.basicConfig(stream=log_file, format='%(levelname)s : %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

class CommandLine:
  def __init__(self):
    self.parser = argparse.ArgumentParser(description = "Description for my parser")
    self.parser.add_argument("-d", "--date", help = "Specify report's date in pattern YYYYMMDD. Example: --d 25641022", required = False, type=str)
    self.parser.add_argument("-t", "--test", help = "Matching Hiweb records and Airtable which records will be updated.", action="store_true")

    self.argument = self.parser.parse_args()
    logger.info(str(vars(self.argument)))