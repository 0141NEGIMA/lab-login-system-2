import os
from dotenv import load_dotenv

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_USER_ID = os.getenv("SLACK_USER_ID")
STATUS_EMOJI = os.getenv("STATUS_EMOJI")


def get_slack_token():
    return SLACK_TOKEN

def get_slack_user_id():
    return SLACK_USER_ID

def get_status_emoji():
    return STATUS_EMOJI