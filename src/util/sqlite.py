import sqlite3
import pandas as pd

DB_NAME = 'db/lab_login_system_2.db'

# テーブルの作成
def init():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    create_member_query = "CREATE TABLE IF NOT EXISTS member (id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, macaddr STRING, notionid STRING)"
    create_record_query = "CREATE TABLE IF NOT EXISTS record (id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, enter_leave STRING, timestamp STRING, foreign key (name) references member(name))"
    cur.execute(create_member_query)
    cur.execute(create_record_query)
    conn.commit()

# DBに登録された全てのメンバーの情報を取得する
def get_all_members_info():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    result = []
    select_query = f"SELECT * FROM member"
    for row in cur.execute(select_query):
        result.append({"name": row[1], "macaddr": row[2], "notionid": row[3]})
    conn.close()
    return result

# 新規メンバーをDBに登録する
def register_member(member_name, mac_addr, notion_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    insert_query = f"INSERT INTO member (name, macaddr, notionid) VALUES ('{member_name}', '{mac_addr}', '{notion_id}');"
    cur.execute(insert_query)
    conn.commit()
    conn.close()

# メンバーをDBから削除する
def delete_member(member_name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    delete_query = f"DELETE FROM member WHERE name = '{member_name}'"
    cur.execute(delete_query)
    conn.commit()
    conn.close()

# 特定のメンバーの入退室記録を取得する
def select_from_record(member_name):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(f"SELECT enter_leave,timestamp FROM record WHERE name='{member_name}'", conn)
    conn.close()
    return df

# 入退室を記録する
def insert_into_record(member_name, enter_leave, timestamp):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    insert_query = f"INSERT INTO record (name, enter_leave, timestamp) VALUES ('{member_name}', '{enter_leave}', '{timestamp}');"
    cur.execute(insert_query)
    conn.commit()
    conn.close()

# テーブルをリセットする
def reset_table(table_name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    delete_query = f"DELETE FROM {table_name};"
    sequence_reset_query = f"DELETE FROM sqlite_sequence WHERE name = '{table_name}';"
    cur.execute(delete_query)
    cur.execute(sequence_reset_query)
    conn.commit()
    conn.close()