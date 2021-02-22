from flask import Flask
from flask_restful import Api
import api.email
from api.user import posts, follow, profile, search
from api.user.Login import login, refresh
import database.mysql_connection
import config
import mysql.connector
import files
from PIL import Image
import os

PORT = 5002
HOST = "0.0.0.0"

"""
WARNING: 
Endpoint classes are not that much documented as all of the documentation is in "api/Api Documentation.md".
Consult that file to get information on how to contact these endpoints in order for you to get access to the right data.
"""

# Creating media directory if doesn't exist :
files.prepare_directory("Medias/profile_picture")
files.prepare_directory("Medias/image")

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Limit contents upload to 5 megabytes.

api_app = Api(app)

# Establishing connection.
database.mysql_connection.cnx = mysql.connector.connect(
    user=config.databaseUserName,
    password=config.password,
    host=config.host,
    database=config.databaseName,
    use_pure=True)
database.mysql_connection.cnx.autocommit = True

# Defining api resources.
api_app.add_resource(login.Login, "/user/login/<username>")
api_app.add_resource(refresh.Refresh, "/user/login/refresh/<refresh_token>")
api_app.add_resource(posts.Post, "/user/post")
api_app.add_resource(search.Search, "/user/search")
api_app.add_resource(follow.Follow, "/user/<id>/follow")
api_app.add_resource(api.email.Email, "/email/<email>/taken")
api_app.add_resource(profile.ProfileUpdate, "/user/profile")
api_app.add_resource(profile.ProfileRetrieving, "/user/<id>/profile/data")
api_app.add_resource(profile.ProfilePicture, "/user/<id>/profile/picture")

if __name__ == "__main__":
    # Running the api.
    app.run(host=HOST, port=PORT, ssl_context=("ApiCertificate/0.0.0.0:5002.crt", "ApiCertificate/0.0.0.0:5002.key"))
