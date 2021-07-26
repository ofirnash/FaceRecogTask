import logging
import threading
from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from services import Service

app = Flask(__name__)
api = Api(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/my-mongodb"
mongo = PyMongo(app)
db_collection = mongo.db.persons  # Persons collection

api.add_resource(Service.post, '/services/add', endpoint="add")
api.add_resource(Service.get, '/services/find', endpoint="find")

if __name__ == '__main__':
    logging.info(msg=f"Start threaded upload to DB - {app.config['MONGO_URI']}")
    threading.Thread(target=Service.threaded_add_to_db, daemon=True).start()
    app.run()
