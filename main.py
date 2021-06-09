from pymongo import collection
from flask import Flask, request
import datetime
from utils import *

app = Flask(__name__)


@app.route('/message', methods=['GET', 'POST', 'DELETE'])
def main():
    meta_data = request.json
    receiver = request.args.get("receiver")
    id = request.args.get("id")
    action = request.args.get("action")
    username = request.args.get("username")
    password = request.args.get("password")

    if request.method == 'POST':
        if login(username, password):
            """ saving data in DB """
            data = datetime.datetime.now()
            meta_data["creation_date"] = data.strftime('%m/%d/%Y')
            meta_data['isRead'] = False
            collection.insert_one(meta_data)
            return f'File with {meta_data["id"]} id successfully added'
        else:
            return 'Username or Password not correct'

    if request.method == 'GET':
        if login(username, password):
            dataDb = collection.find()
            search_data = [data for data in dataDb if data["receiver"].lower() == receiver.lower()]
            result = action_options.get(action, None)(search_data, id)
            if result:
                return result
        else:
            return 'Username or Password not correct'

    if request.method == 'DELETE':
        if login(username, password):
            collection.delete_one({"id": id})
            return f'File with {id} id deleted'
        else:
            return 'Username or Password not correct'


if __name__ == '__main__':
    app.run()
