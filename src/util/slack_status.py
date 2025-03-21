import requests
from config import get_slack_token, get_slack_user_id, get_status_emoji

def update_slack_status(user_id=None, clear=False):
    """
    Slackのステータスを更新または削除する関数
    
    Args:
        user_id (str, optional): 更新するユーザーのID
        status_emoji (str, optional): 設定するステータス絵文字
        clear (bool, optional): Trueの場合、ステータスを削除する
        
    Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
    """

    user_id = get_slack_user_id()
    slack_token = get_slack_token()
    status_emoji = get_status_emoji()

    
    url = "https://slack.com/api/users.profile.set"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    # clearフラグがTrueならstatus削除
    if clear:
        data = {
            "user": user_id,
            "profile": {
                "status_text": "",
                "status_emoji": ""
            }
        }
        action_text = "Status cleared"
    else:
        data = {
            "user": user_id,
            "profile": {
                "status_emoji": status_emoji
            }
        }
        action_text = "Status updated"
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200 and response.json().get("ok"):
        print(f"{action_text} successfully.")
        return True
    else:
        print(f"Failed to {action_text.lower()}:", response.json().get("error"))
        return False
    
if __name__ == "__main__":
    
    clear = False
    
    # ステータス更新を実行
    update_slack_status(clear=clear)