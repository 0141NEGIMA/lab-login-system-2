from notion_client import Client
from util.config import get_notion_token, get_database_id
from datetime import datetime

NOTION_TOKEN = get_notion_token()
DATABASE_ID = get_database_id()
client = Client(auth=NOTION_TOKEN)

def get_all_members_info():
    response = client.databases.query(
        database_id=DATABASE_ID
    )
    return [{"notionid": member["id"], "status": member["properties"]["入退室状況"]["status"]["name"], "total": member["properties"]["累計（分）"]["number"], "entry_time": member["properties"]["入室時刻"]["date"]} for member in response["results"]]

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
    
def set_total_minutes(page_id, total_minutes):
    client.pages.update(
        page_id=page_id,
        properties = {
            "累計（分）": {
                "number": total_minutes
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

def get_total_minutes():
    response = client.databases.query(
        database_id=DATABASE_ID
    )
    return {member["properties"]["名前"]["title"][0]["plain_text"]: member["properties"]["累計（分）"]["number"] for member in response["results"]}

def reset_total_minutes():
    ids = [member['notionid'] for member in get_all_members_info()]
    for id in ids:
        set_total_minutes(id, 0)

def set_entry_time(page_id):
    response = client.pages.update(
        page_id=page_id,
        properties={
            "入室時刻": {
                "date": {
                    "start": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00")
                }
            }
        }
    )

def reset_entry_time():
    members = get_all_members_info()
    for member in members:
        if member['entry_time'] != None:
            response = client.pages.update(
                page_id=member['notionid'],
                properties={
                    "入室時刻": {
                        "date": None
                    }
                }
            )