from flask import Flask
from flask_pymongo import PyMongo
import os
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    #creates a flask app to be loaded locally when running program
    app.secret_key = os.getenv("FLASKAPIKEY")
    app.config["MONGO_URI"] = "mongodb://localhost:27017/immaculate_db"
    # our db controller
    # access db through mongo.db, collections through mongo.db.collection_name

    mongo.init_app(app)

    # imports have to be here since create_app() runs once, otherwise circular dependency
    from code.controllers import api
    from code.services.player_service import PlayerService
    from code.services.question_service import QuestionService
    app.player_service = PlayerService()
    app.question_service = QuestionService()
    app.register_blueprint(api)


    return app