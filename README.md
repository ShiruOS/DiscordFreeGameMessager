# DiscordFreeGameMessager
It automatically sends free game news to discord channel using discord webhooks
Fires using Git-Hub Actions everyday
Keeps data in the cloud DB

This uses gamerpower.com's api to get news and filters out to send giveaways from GOG, Steam and Epic games. This can be changed from ```Setting.json```
## Setting up
This sections covers setting up this project on your github actions
### Database
This project uses Supabase for the database to make sure that the bot does post a game which it has already posted. create a table with id(int8), end(date) and title(txt)
### Secrets
Use github secretes to keep your credentials safe