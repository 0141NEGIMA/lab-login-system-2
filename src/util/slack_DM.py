import requests
import argparse
import os
import sys
from util.config import get_slack_bot_token

def send_slack_dm_with_image(user_id=None, user_name=None, image_path=None, message=None, bot_token=None):
    """
    Slackボットから特定のユーザーにDMを送信する関数（テキストのみ、画像のみ、または両方）
    
    Args:
        user_id (str, optional): メッセージを送信するユーザーのID
        user_name (str, optional): メッセージを送信するユーザーの名前（CSV参照用）
        image_path (str, optional): 送信する画像ファイルのパス（省略可）
        message (str, optional): 送信するメッセージの内容（省略可）
        bot_token (str, optional): SlackボットのOAuthトークン
        csv_path (str, optional): メンバーデータのCSVファイルパス
        
    Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
    """
    # トークンの取得（引数かconfigから）
    bot_token = bot_token or get_slack_bot_token()
    
    if not bot_token:
        print("Error: Bot token not found. Please set SLACK_BOT_TOKEN in .env file.")
        return False
    
    if not user_id:
        print("Error: Either user_id or user_name is required.")
        return False
    
    # メッセージも画像も指定されていない場合はエラー
    if not message and not image_path:
        print("Error: Either message or image_path must be provided.")
        return False
    
    # 画像パスが指定されている場合は存在チェック
    if image_path and not os.path.exists(image_path):
        print(f"Error: Image file not found at path: {image_path}")
        return False
    
    # まずDMチャンネルを開く
    open_response = requests.post(
        "https://slack.com/api/conversations.open",
        headers={
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json"
        },
        json={"users": user_id}
    )
    
    if not open_response.status_code == 200 or not open_response.json().get("ok"):
        print(f"Failed to open DM channel: {open_response.json().get('error')}")
        return False
    
    # DMチャンネルIDを取得
    channel_id = open_response.json().get("channel", {}).get("id")
    
    # メッセージを送信（指定されている場合）
    if message:
        message_response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {bot_token}",
                "Content-Type": "application/json"
            },
            json={
                "channel": channel_id,
                "text": message
            }
        )
        
        if not message_response.status_code == 200 or not message_response.json().get("ok"):
            print(f"Warning: Failed to send message: {message_response.json().get('error')}")
            if not image_path:  # メッセージのみの送信で失敗した場合
                return False
    
    # 画像が指定されている場合のみアップロード処理
    if image_path:
        try:
            # 1. ファイル情報の取得
            filename = os.path.basename(image_path)
            file_size = os.path.getsize(image_path)
            
            # 2. アップロードURLの取得
            get_url_response = requests.get(
                f"https://slack.com/api/files.getUploadURLExternal",
                headers={
                    "Authorization": f"Bearer {bot_token}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                params={
                    "filename": filename,
                    "length": file_size
                }
            )
            
            url_data = get_url_response.json()
            
            if not url_data.get("ok"):
                print(f"Failed to get upload URL: {url_data.get('error')}")
                return message is not None  # メッセージがあれば部分的成功
            
            upload_url = url_data["upload_url"]
            file_id = url_data["file_id"]
            
            # 3. アップロード実行
            with open(image_path, 'rb') as file:
                file_content = file.read()
                
                upload_response = requests.post(
                    upload_url,
                    data=file_content
                )
            
            if upload_response.status_code != 200:
                print(f"Failed to upload file: {upload_response.status_code} {upload_response.text}")
                return message is not None  # メッセージがあれば部分的成功
            
            # 4. アップロード完了処理
            complete_payload = {
                "files": [{"id": file_id, "title": filename}],
                "channel_id": channel_id
            }
            
            complete_response = requests.post(
                "https://slack.com/api/files.completeUploadExternal",
                headers={
                    "Authorization": f"Bearer {bot_token}",
                    "Content-Type": "application/json; charset=utf-8"
                },
                json=complete_payload
            )
            
            complete_data = complete_response.json()
            
            if complete_data.get("ok"):
                name_display = f"'{user_name}'" if user_name else f"ID '{user_id}'"
                print(f"Image sent successfully to user {name_display}")
                return True
            else:
                print(f"Failed to complete upload: {complete_data.get('error')}")
                return message is not None  # メッセージがあれば部分的成功
                
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return message is not None  # メッセージがあれば部分的成功
    
    return True  # メッセージのみで成功した場合

if __name__ == "__main__":
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='SlackボットからDMを送信するツール')
    parser.add_argument('--user', type=str, help='送信先ユーザーのID（--nameと排他）')
    parser.add_argument('--name', type=str, help='送信先ユーザーの名前（CSV参照用）')
    parser.add_argument('--image', type=str, help='送信する画像ファイルのパス（省略可）')
    parser.add_argument('--message', type=str, help='送信するメッセージ（省略可）')
    parser.add_argument('--token', type=str, help='SlackボットのOAuthトークン（省略時は.envから取得）')
    parser.add_argument('--csv', type=str, default="member_data.csv", help='メンバーデータのCSVファイルパス（デフォルト: member_data.csv）')
    
    args = parser.parse_args()
    
    # 引数のチェック
    if not args.user and not args.name:
        print("Error: Either --user or --name must be specified.")
        sys.exit(1)
    
    if args.user and args.name:
        print("Warning: Both --user and --name are specified. --name will be ignored.")
    
    # DMを送信
    send_slack_dm_with_image(
        user_id=args.user,
        user_name=args.name if not args.user else None,  # userが指定されている場合はnameを無視
        image_path=args.image,
        message=args.message,
        bot_token=args.token,
        csv_path=args.csv
    )