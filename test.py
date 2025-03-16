import sqlite3

# DBの作成
dbname = 'test.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# テーブルの作成
create_table_query = "CREATE TABLE IF NOT EXISTS person(id INTEGER PRIMARY KEY AUTOINCREMENT, name STING)"
cur.execute(create_table_query)

# 行の挿入
insert_query = "INSERT INTO person (name) VALUES ('taro')"
cur.execute(insert_query)

# 変更の反映
conn.commit()
conn.close()
