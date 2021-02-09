from flask import Flask, request, jsonify
from dotenv import load_dotenv
import pymongo

load_dotenv(dotenv_path='../.env')
app = Flask(__name__)
client = pymongo.MongoClient(os.getenv('DB_CONNECTION_STRING'))
db = client['db']['articles']

@app.route('/search', methods=['POST'])
def search():
    results = db.find(request.json)
    res = [modify_res(i) for i in results]
    return jsonify(res), 200


def modify_res(item):
    item['_id'] = str(item['_id'])
    return item


if __name__ == '__main__':
    app.run()  # run our Flask app