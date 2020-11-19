from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_db(app):
    app.config["MONGODB_SETTINGS"] = {
    "host": app.config.get("MOGNODB")
    }
    db.init_app(app)

