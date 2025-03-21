import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

SLACK_USER_NAME = os.getenv("SLACK_USER_NAME")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_USER_ID = os.getenv("SLACK_USER_ID")
STATUS_EMOJI = os.getenv("STATUS_EMOJI")

def get_notion_token():
    return NOTION_TOKEN

def get_database_id():
    return DATABASE_ID

def get_slack_user_name():
    return SLACK_USER_NAME

def get_slack_token():
    return SLACK_TOKEN

def get_slack_user_id():
    return SLACK_USER_ID

def get_status_emoji():
    return STATUS_EMOJI