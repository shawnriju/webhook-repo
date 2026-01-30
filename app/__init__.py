from flask import Flask

from app.webhook.routes import webhook
from app.extensions import mongo


# Creating our flask app
def create_app():

    app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
    )
    
    # MongoDB configuration
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"

    # Initialize MongoDB
    mongo.init_app(app)

    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
