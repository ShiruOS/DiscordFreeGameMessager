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


def GetData(column):
    """Gets data from database about specific column and returns an arry"""
    data = []
    res = supabase.table(tableName).select(column).execute()

    for i in (
        res.data
    ):  # Gets the data in form of dict nested in array and coverts into array of id
        data.append(i[column])
    print("Data recived from db")
    return data


def InsertData(data: dict):
    """Enters new row into the db"""
    print("Inserting data")
    end: str = data["end"]
    if (
        "N" in end
    ):  # Checks if any game has expiry date as N/A and if yes then sets it to a week in future
        today = datetime.now()
        end = (today + timedelta(days=7)).strftime("%Y-%m-%d")
    else:
        end = end.split()[0]  # If not N/A then spilts date from time

    supabase.table(tableName).insert(
        {"id": data["id"], "end": end, "title": data["title"]}
    ).execute()


def DeleteData(column: str, data):
    """Deletes old data when data from column matches"""
    res = supabase.table(tableName).delete().eq(column, data).execute()
    print(res)
    return res
