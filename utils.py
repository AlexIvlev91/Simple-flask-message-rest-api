import json
from pymongo import MongoClient

try:
    cluster = MongoClient(
        "mongodb+srv://phantom:y68qtE8SMRevBA2M@cluster0.uyud2.mongodb.net/md5?retryWrites=true&w=majority")
    db = cluster["message"]
    collection = db["message_api"]

except:
    print("Could not connect to MongoDB")


def get_all_data(search_data: dict, id):
    message = []
    for data in search_data:
        del data["_id"]
        message.append(data)
    return json.dumps(message)


def read_message(search_data: dict, id):
    for data in search_data:
        if data["id"] == id:
            del data["_id"]
            collection.update_one({"id": data["id"]}, {"$set": {"isRead": True}})
            return json.dumps(data)


def get_unread_file(search_data: dict, id):
    message = []
    for data in search_data:
        if not data["isRead"]:
            del data["_id"]
            message.append(data)
    return json.dumps(message)


action_options = {"all": get_all_data,
                  "read": read_message,
                  "unread": get_unread_file
                  }


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1, username='username', password='password'))


def login(username, password):
    user = [x for x in users if x.username == username][0]
    if user and user.password == password:
        return True
