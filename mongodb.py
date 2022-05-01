from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://codingkitten:pgbZrSeXYgtrz7II@cluster0.8dgma.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
    server_api=ServerApi("1"),
)

client.test.command("count", "test")
