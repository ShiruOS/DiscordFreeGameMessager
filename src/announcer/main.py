import datetime
import os

import ApiHandler
import DB
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL")
NEWS_API = os.getenv("NEWS_API")
CRASH_BOY = os.getenv("CRASH_BOY")

ApiHandler.CrashBoy("Game Announcer begin", CRASH_BOY)

endDates = ids = DB.GetData("end")
for date in endDates:
    end_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    today = datetime.date.today()
    if end_date < today:
        DB.DeleteData("end", date)


content: list = ApiHandler.GetNews(NEWS_API)
ids = DB.GetData("id")

if content:
    for row in content:
        if row["id"] not in ids:
            end_date = row["end"].split()[0]
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            today = datetime.date.today()
            if end_date < today:
                continue
            DB.InsertData(row)
            ApiHandler.SendToDiscord(row, DISCORD_WEBHOOK_URL)

ApiHandler.CrashBoy("Game Announcer End", CRASH_BOY)
