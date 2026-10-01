from flask import Flask
from flask_pymongo import PyMongo
import os
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    #creates a flask app to be loaded locally when running program
    app.secret_key = os.getenv("FLASKAPIKEY")
    app.config["env"] = os.getenv("ENVIRONMENT")

    # defaults to docker host on 27017 if no env var
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)
    mongo.db = mongo.cx[f"{os.getenv('MONGO_DB_CONN')}"]
    # our db controller
    # access db through mongo.db, collections through mongo.db.collection_name

    # imports have to be here since create_app() runs once, otherwise circular dependency
    from immaculate_api.controllers import api
    from immaculate_api.services.player_service import PlayerService
    from immaculate_api.services.question_service import QuestionService
    app.player_service = PlayerService()
    app.question_service = QuestionService()
    app.register_blueprint(api)


    return app