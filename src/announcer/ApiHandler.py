import time

import requests
from discord_webhook import DiscordWebhook


def GetNews(URL: str):
    """Fecthes data from api then parses into useable format"""
    data = None
    content = []

    try:
        res = requests.get(URL)
        if res.status_code == 200:
            print("Data Recived from API")
            data = res.json()
        else:
            print("Error:", res.status_code)

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    if data:
        print("Parshing...")
        for row in data:
            content.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "platform": row["platforms"],
                    "description": row["description"],
                    "end": row["end_date"],
                    "open_giveaway_url": row["open_giveaway_url"],
                }
            )

        return content
    return None


def SendToDiscord(content: dict, DISCORD_WEBHOOK_URL: str):
    """Produces a useable message that uses dict and sends it to discord"""
    print("sending news to discod")
    msg = (
        f"> **Game:** {content['title']}\n"
        f"> **Platform:** {content['platform']}\n"
        f"**[CLAIM HERE]({content['open_giveaway_url']})**\n"
        f"*Expires {content['end']}*"
    )
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=msg)
    webhook.execute()
    time.sleep(1)


def CrashBoy(msg: str, URL: str):
    """Sends Crashboy message"""
    webhook = DiscordWebhook(url=URL, content=msg)
    webhook.execute()
