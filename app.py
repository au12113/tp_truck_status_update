import logging
import prog_options

from dotenv import dotenv_values
from pytz import timezone
from datetime import datetime
from pyairtable import Table

from hiweb_sql import get_hiweb_stock

def get_month_pattern(specific_date=None):
  date = datetime.now() if specific_date == None else datetime(year=int(specific_date[0:4])-543, month=int(specific_date[4:6]), day=int(specific_date[6:8]))
  thai_tz = timezone('Asia/Bangkok')
  loc_dt = thai_tz.localize(date)
  return str(loc_dt.year + 543) + str(loc_dt.month).zfill(2) + '%'

config = dotenv_values(".env")
arg = prog_options.CommandLine()

logger = logging.getLogger('__main__')

month_pattern = get_month_pattern(arg.argument.date)
current_stock = get_hiweb_stock(db_config=config, month_pattern=month_pattern)
enginno_list = current_stock['enginno'].unique()
api_key = config.get('AIRTABLE_API_KEY')
table = Table(api_key, base_id=config.get('AIRTABLE_BASE_ID'), table_name=config.get('AIRTABLE_TABLE_ID'))
for enginno in enginno_list:
  formula = "LEFT({เลขเครื่อง}, 6)='"+str(enginno)+"'"
  fetched = table.all(formula=formula)
  for target in fetched:
    source = current_stock.loc[current_stock['enginno']==enginno]
    if ('เลขสัญญาขาย' not in target.get('fields')) or ('วันที่ตัดขาย' not in target.get('fields')):
      date_string = source['stockdate'].values[0]
      source_date = datetime(year=int(date_string[0:4]), month=int(date_string[4:6]), day=int(date_string[6:8]))
      if arg.argument.test == True:
        logger.info(target.get('fields')['เลขเครื่อง'] + " will update " + str({ "เลขสัญญาขาย": source['stockno'].values[0], "วันที่ตัดขาย": source_date.isoformat() }))
      else:
        table.update(target.get('id'), { "เลขสัญญาขาย": source['stockno'].values[0], "วันที่ตัดขาย": source_date.isoformat()})
        logger.info("Update " + target.get('fields')['เลขเครื่อง'] + " with " + str({ "เลขสัญญาขาย": source['stockno'].values[0], "วันที่ตัดขาย": source_date.isoformat()}))
    # else:
    #   print(target.get('id'), "already got update")
