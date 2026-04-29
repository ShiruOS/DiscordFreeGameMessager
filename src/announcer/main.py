import datetime
import os

import ApiHandler
import DB
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL")
NEWS_API: str = os.getenv("NEWS_API")
CRASH_BOY: str = os.getenv("CRASH_BOY")  # This one sends log to private discord channel

ApiHandler.CrashBoy("Game Announcer begin", CRASH_BOY)

# Deletes the entries which are expired
try:
    endDates = ids = DB.GetData("end")
    for date in endDates:
        end_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        today = datetime.date.today()
        if end_date < today:
            DB.DeleteData("end", date)
except Exception as err:
    ApiHandler.CrashBoy(str(err), CRASH_BOY)

# Gets the latest free game news froms the source(www.gamerpower.com)
content = None
ids = None
try:
    content = ApiHandler.GetNews(NEWS_API)
    ids = DB.GetData("id")
except Exception as err:
    ApiHandler.CrashBoy(str(err), CRASH_BOY)

# Checks the news to see if any new enties, by comparing to previous one
try:
    if content:
        for row in content:
            if row["id"] not in ids:
                DB.InsertData(row)
                ApiHandler.SendToDiscord(row, DISCORD_WEBHOOK_URL)
except Exception as err:
    ApiHandler.CrashBoy(str(err), CRASH_BOY)
