import mysql.connector
import util.notion as notion

# ユーザ名の入力
user_name = input("Enter name to delete: ")
confirmation = input(f"Are you sure you want to delete {user_name}? y/[n]: ")
if confirmation == "y":
    print(f"Deleting {user_name}...")
    
    # notionから削除
    notion.delete_member(user_name)

    # MySQLに接続
    conn = mysql.connector.connect(
        host="localhost",
        user="sqladmin",
        password="sqladmin",
        database="lab_login_system_2"
    )
    cursor = conn.cursor()

    # MySQLから削除
    delete_query = f"DELETE FROM member WHERE name = '{user_name}'"
    cursor.execute(delete_query)
    conn.commit()
    
    # MySQLとの接続を閉じる
    cursor.close()
    conn.close()

    print(f"{user_name} was deleted from DB.")
else:
    print("Interrupted. Nothing has changed.")