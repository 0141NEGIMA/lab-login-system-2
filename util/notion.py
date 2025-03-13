from notion_client import Client
import os

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = "1b5d342275f38044be36c711e2de4c87"
client = Client(auth=NOTION_TOKEN)

def get_member_ids():
    response = client.databases.query(
        database_id=DATABASE_ID
    )
    return [{"id": member["id"], "status": member["properties"]["入退室状況"]["status"]["name"], "total": member["properties"]["累計（分）"]["number"]} for member in response["results"]]

def enter_room(page_id):
    response = client.pages.update(
        page_id=page_id,
        properties={
            "入退室状況": {
                "status": {
                    "name": "入室"
                }
            }
        }
    )

def leave_room(page_id):
    response = client.pages.update(
        page_id=page_id,
        properties={
            "入退室状況": {
                "status": {
                    "name": "退室"
                }
            }
        }
    )

def create_member(member_name):
    response = client.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "名前": {
                "title": [
                    {
                        "text": {
                            "content": member_name
                        }
                    }
                ]
            },
            "入退室状況": {
                "status": {
                    "name": "入室"
                }
            },
            "累計（分）": {
                "number": 0
            }
        }
    )
    print(f"Notion: Welcome {member_name}!")
    return(response["id"])

def delete_member(member_name):
    response = client.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "名前",
            "title": {
                "equals": member_name
            }
        }
    )
    if response["results"]:
        for page in response["results"]:
            page_id = page["id"]
            client.pages.update(
                page_id=page_id,
                archived=True
            )
        print(f"Notion: {member_name} has archived.")
        return 0
    else:
        print(f"Notion: {member_name} was not found.")
        return 1