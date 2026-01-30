from flask import Flask
import os
from dotenv import load_dotenv

from app.webhook.routes import webhook
from app.extensions import mongo

load_dotenv()

# Creating our flask app
def create_app():

    app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
    )
    
    # MongoDB configuration
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    # Initialize MongoDB
    mongo.init_app(app)

    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
