import os

from dotenv import load_dotenv

import ApiHandler

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

NEWS_API = os.getenv("NEWS_API")

print("""Welcome
      starting the server
      """)

content = ApiHandler.GetNews(NEWS_API)
print(content)
# ApiHandler.SendToDiscord(content, DISCORD_WEBHOOK_URL)
