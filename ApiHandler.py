# import parser

import requests
from discord_webhook import DiscordWebhook


def GET_API_RES(URL: str):
    try:
        res = requests.get(URL)
        if res.status_code == 200:
            print("Data Recived")
            return res.json()
        else:
            print("Error:", res.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def GetJokes(API_URL: str):
    post = GET_API_RES(API_URL)
    if post:
        if "joke" in post.keys():
            print(post["joke"])
            content = post["joke"]
            return content
        elif "setup" in post.keys() and "delivery" in post.keys():
            print(post["setup"])
            print(post["delivery"])
            content = f"{post['setup']} \n \n {post['delivery']}"
            return content
        else:
            return None


def SendToDiscord(msg: str, DISCORD_WEBHOOK_URL: str):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=msg)
    res = webhook.execute()

    print("Message sent\n", res)


def GetNews(API_URL: str):
    post = GET_API_RES(API_URL)
    # parser.parse(post)
    content = ""
    if post:
        print("Processing...")
        for data in post:
            content += f"Title:{data['title']}\nPlatform:{data['platforms']}\nDescription:{data['description']}\n\n"

        content += "This is an auto-generated message please contact the operator in case of any issues \n*Source*:https://www.gamerpower.com"

        return content
    return None
