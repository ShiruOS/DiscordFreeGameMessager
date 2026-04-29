import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
tableName: str = os.environ.get("TABLE")

supabase: Client = create_client(url, key)
res = None


def GetData(column: str):
    data = []
    res = supabase.table(tableName).select(column).execute()

    for i in res.data:
        data.append(i[column])
    print("Data recived from db")
    return data


def InsertData(data: dict):
    print("Inserting data")
    end: str = data["end"]
    if "N" in end:
        today = datetime.now()
        end = (today + timedelta(days=7)).strftime("%Y-%m-%d")
    else:
        end = end.split()[0]

    res = (
        supabase.table(tableName)
        .insert({"id": data["id"], "end": end, "title": data["title"]})
        .execute()
    )
    return res


def DeleteData(column: str, data):
    res = supabase.table(tableName).delete().eq(column, data).execute()
    print(res)
    return res
