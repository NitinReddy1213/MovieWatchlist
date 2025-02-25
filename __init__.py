import os  #used to host the application
from flask import Flask  #used for backend wsgi server
from dotenv import load_dotenv  # usde to connect database keys from file
from pymongo import MongoClient  #MongoDB client 
from movie_library.routes import pages 

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
  app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY",
             "8a1a81353a9e03f01ba854a5c05aa127cd7088430b539bcb357a20c16105f5ba")
  app.db = MongoClient(app.config["MONGODB_URI"]).movies

  app.register_blueprint(pages)
  return app








