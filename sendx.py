"""
json: Format the data to be sent by the Twitter API into JSON
requests: HTTP client
"""
import os
from os.path import join, dirname
import json
from datetime import datetime
from dotenv import load_dotenv
import tweepy
import pytz
# from decimal import Decimal, ROUND_HALF_UP

jst = pytz.timezone('Asia/Tokyo')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
load_dotenv(verbose=True)

# 各種twitterのKeyをセット CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# tweepyの設定
# auth = tweepy.Client(BEARER_TOKEN)
auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# auth = tweepy.OAuth2AppHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)
client_t = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)


"""
Notification Class to configure the settings for the Twitter API
"""
def post(text):
    """
    POST request to Twitter API
    API docs: https://developer.twitter.com/en/docs/twitter-api/api-reference-index
    """
    # The name of the file you"re going to upload
    # file = open(f"/tmp/{self.date}.jpg", "rb")
    # title = f"{self.date}.jpg"
    # Call the files.upload method using the WebClient
    # Uploading files requires the `files:write` scope
    try:
        client_t.create_tweet(
            text=text,
        )        # file_names = ["/tmp/" + title, ]
        # media_ids = []
        # for filename in file_names:
        #     res = api.media_upload(filename=filename)
        #     media_ids.append(res.media_id)
        #     api.create_media_metadata(res.media_id, title)
        # tweet with multiple images
        # client_t.create_tweet(
        #     text=text,
        #     media_ids=media_ids,
        # )
    except Exception as e:
        print(e)


def format_text(json_data):
    """
    Create params data for sending Twitter notification with API.
    """
    # Webサーバから受け取ったJSONを辞書に変換する
    json_data = json.loads(json_data)
    # 緊急地震速報かつ第一報かつ予想震度3以上なら処理させる
    # get first eew message
    if json_data.get('type') == 'eew' and json_data.get('report') == '1' and str(json_data.get('intensity')) > '0':
        # get EQ Data
        dt = json_data.get('time')[:-3]
        dt = datetime.fromtimestamp(int(dt)).astimezone(jst)
        magnitude = float(json_data.get('magnitude'))
        epicenter = str(json_data.get('epicenter'))
        depth = str(json_data.get('depth'))
        intensity = str(json_data.get('intensity'))

        text = """
            地　震　速　報　（第１報）

            日　　時　　：　　{0}
            震　　源　　：　　{1}
            予想震度　　：　　{2}
            規　　模　　：　　M{3}
            深　　さ　　：　　{4}

            """.format(dt, epicenter, intensity, str(magnitude), depth)

        post(text)

        return

    elif json_data.get('type') == 'eew' and json_data.get('report') == 'final' and str(json_data.get('intensity')) > '0':
        # get EQ Data
        dt = json_data.get('time')[:-3]
        dt = datetime.fromtimestamp(int(dt)).astimezone(jst)
        magnitude = float(json_data.get('magnitude'))
        epicenter = str(json_data.get('epicenter'))
        depth = str(json_data.get('depth'))
        intensity = str(json_data.get('intensity'))

        text = """
            地　震　速　報　（最終報）

            日　　時　　：　　{0}
            震　　源　　：　　{1}
            予想震度　　：　　{2}
            規　　模　　：　　M{3}
            深　　さ　　：　　{4}

            """.format(dt, epicenter, intensity, str(magnitude), depth)

        post(text)

    # 誤報の場合はpga_alert_cancelが送られてくる「らしい」のでそちらも検知するようにする
    # Alert Cancel
    elif json_data.get('type') == 'pga_alert_cancel':
        text = 'さきほどの震度速報はキャンセルされました。'

        post(text)

        return

    else:
        pass
