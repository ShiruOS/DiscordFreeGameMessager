import datetime
import json
import os

import DB
import Util
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL")  # This sends msg to the consumer channel
CRASH_BOY: str = os.getenv("CRASH_BOY")  # This sends log to private discord channel


NEWS_API = ""
PLATFORM = []
with open("setting.json", "r") as f:
    data = json.load(f)
    NEWS_API = data["source"]
    PLATFORMS = data["platforms"]


Util.SendMsg("Game Announcer begin", CRASH_BOY)

# Deletes the entries which are expired
try:
    endDates = DB.GetData("end")
    today = datetime.date.today()
    for date in endDates:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if end_date < today:
            DB.DeleteData("end", date)
except Exception as err:
    Util.SendMsg(str(err), CRASH_BOY)

# Gets the latest free game news froms the source(www.gamerpower.com)
content = None
ids = None
try:
    content = Util.GetNews(NEWS_API)
    ids = DB.GetData("id")
except Exception as err:
    Util.SendMsg(str(err), CRASH_BOY)
else:
    # Checks the news to see if any new enties, by comparing to previous one
    print("searching.....")
    try:
        if content:
            for row in content:
                if Util.CheckPlatform(row["platform"], PLATFORMS):
                    if row["id"] not in ids:
                        DB.InsertData(row)
                        Util.Post(row, DISCORD_WEBHOOK_URL)
    except Exception as err:
        Util.SendMsg(str(err), CRASH_BOY)
finally:
    Util.SendMsg("Process Done", CRASH_BOY)
