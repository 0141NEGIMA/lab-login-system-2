import sqlite3

DB_NAME = 'db/lab_login_system_2.db'
TABLE_NAME = "member"

# DBの作成または接続
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# テーブルの作成
def init():
    create_table_query = "CREATE TABLE IF NOT EXISTS member (id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, macaddr STRING, notionid STRING)"
    cur.execute(create_table_query)
    conn.commit()

# DBに登録された全てのメンバーの情報を取得する
def get_all_members_info():
    result = []
    select_query = f"SELECT * FROM {TABLE_NAME}"
    for row in cur.execute(select_query):
        result.append({"name": row[1], "macaddr": row[2], "notionid": row[3]})
    return result

# 新規メンバーをDBに登録する
def register_member(member_name, mac_addr, notion_id):
    insert_query = f"INSERT INTO {TABLE_NAME} (name, macaddr, notionid) VALUES ('{member_name}', '{mac_addr}', '{notion_id}');"
    cur.execute(insert_query)
    conn.commit()

# メンバーをDBから削除する
def delete_member(member_name):
    delete_query = f"DELETE FROM member WHERE name = '{member_name}'"
    cur.execute(delete_query)
    conn.commit()

conn.close()