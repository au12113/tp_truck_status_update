import psycopg2
import sys
import pandas as pd

def get_hiweb_stock(db_config, month_pattern):
  sql_string = generate_sqlstring(month_pattern)
  sql_cur = query(db_config, sql_string)
  return pd.DataFrame([i for i in sql_cur], columns=[desc[0] for desc in sql_cur.description])

def generate_sqlstring(month_pattern):
  f = open('./hiweb_stock.sql', 'r', encoding='utf-8')
  sql_string = f.read() + f"\n\tand s1.stockdate like '{month_pattern}'"
  f.close()
  return sql_string

def query(db_config, sql_string):
  try:
    conn = psycopg2.connect(
      user=db_config.get('DB_USER'),
      password=db_config.get('DB_PASSWORD'),
      host=db_config.get('DB_HOST'),
      port=db_config.get('DB_PORT'),
      database=db_config.get('DB_NAME')
    )
  except psycopg2.Error as e:
    print(f"Error connecting to Postgres platform: {e}")
    sys.exit(1)

  cur = conn.cursor()
  cur.execute(sql_string)
  return cur
  