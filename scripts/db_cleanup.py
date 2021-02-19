import pymongo
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')
client = pymongo.MongoClient(os.getenv('DB_CONNECTION_STRING'))
db = client['db']['articles']

filter = {"date": {"$lt": datetime.now() - timedelta(hours=24)}} # 24+ hours ago
print('Deleting ' + str(db.count_documents(filter)) + ' articles.')
db.delete_many(filter)
