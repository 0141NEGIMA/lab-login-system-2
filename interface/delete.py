import util.notion as nt
import util.sqlite as sql

# ユーザ名の入力
member_name = input("Enter name to delete: ")
confirmation = input(f"Are you sure you want to delete {member_name}? y/[n]: ")
if confirmation == "y":
    print(f"Deleting {member_name}...")
    
    # notionから削除
    nt.delete_member(member_name)
    
    # SQLiteから削除
    sql.delete_member(member_name)

    print(f"{member_name} was deleted from DB.")
else:
    print("Interrupted. Nothing has changed.")