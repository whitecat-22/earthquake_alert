"""
json: Format the data to be sent by the SLack API into JSON
requests: HTTP client
"""
import os
from os.path import join, dirname
import json
from datetime import datetime
from dotenv import load_dotenv
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pytz
#from decimal import Decimal, ROUND_HALF_UP

jst = pytz.timezone('Asia/Tokyo')

dotenv_path = join(dirname(__file__), '.env')
#load_dotenv(dotenv_path)
load_dotenv(verbose=True)
# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
# ID of channel that you want to upload file to
load_dotenv(dotenv_path)
token = os.environ.get("SLACK_BOT_TOKEN")
channel_id = os.environ.get("SLACK_CHANNEL_ID")


"""
Notification Class to configure the settings for the Slack API
"""
def post(text):
    """
    POST request to Slack file upload API
    API docs: https://slack.com/api/files.upload
    """
    # The name of the file you're going to upload
    # file = open(f"/tmp/{str(self.date)}.png", 'rb')
    # title = f"{str(self.date)}.png"
    # Call the files.upload method using the WebClient
    # Uploading files requires the `files:write` scope
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=text,
        )
        # client.files_upload(
        #     channels=channel_id,
        #     initial_comment=text,
        #     file=file,
        #     title=title
        # )
    except Exception as e:
        print(e)


def format_text(json_data):
    """
    Create params data for sending Slack notification with API.
    """
    # Webサーバから受け取ったJSONを辞書に変換する
    json_data = json.loads(json_data)
    print(json_data)
    # 緊急地震速報かつ第一報かつ予想震度3以上なら処理させる
    # get first eew message
    if json_data.get('type') == 'eew' and json_data.get('report') == '1' and str(json_data.get('intensity')) > '0':
        # get EQ Data
        try:
            dt = json_data.get('time')[:-3]
            dt = datetime.fromtimestamp(int(dt)).astimezone(jst)
        except Exception as e:
            print(e)
            dt = "-"
        magnitude = float(json_data.get('magnitude'))
        epicenter = str(json_data.get('epicenter'))
        depth = str(json_data.get('depth'))
        intensity = str(json_data.get('intensity'))

        text = f"地震速報（第１報）\n\n" \
            f"日　　時：{dt}\n" \
            f"震　　源：{epicenter}\n" \
            f"予想震度：{intensity}\n" \
            f"規　　模：M{str(magnitude)}\n" \
            f"深　　さ：{depth}"

        post(text)

    elif json_data.get('type') == 'eew' and json_data.get('report') == 'final' and str(json_data.get('intensity')) > '0':
        # get EQ Data
        try:
            dt = json_data.get('time')[:-3]
            dt = datetime.fromtimestamp(int(dt)).astimezone(jst)
        except Exception as e:
            print(e)
            dt = "-"
        magnitude = float(json_data.get('magnitude'))
        epicenter = str(json_data.get('epicenter'))
        depth = str(json_data.get('depth'))
        intensity = str(json_data.get('intensity'))

        text = f"地震速報（最終報）\n\n" \
            f"日　　時：{dt}\n" \
            f"震　　源：{epicenter}\n" \
            f"予想震度：{intensity}\n" \
            f"規　　模：M{str(magnitude)}\n" \
            f"深　　さ：{depth}"

        post(text)

    # 誤報の場合はpga_alert_cancelが送られてくる「らしい」のでそちらも検知するようにする
    # Alert Cancel
    elif json_data.get('type') == 'pga_alert_cancel':
        text = "さきほどの震度速報はキャンセルされました。"

        post(text)

    else:
        pass
