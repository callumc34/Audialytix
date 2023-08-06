#!/usr/bin/env python
import os, os.path

from dotenv import load_dotenv
from flask import Flask
from tempfile import gettempdir

from controllers.main import main

# Setup development env variables
load_dotenv()

# Flask variables
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 5000)
DEBUG = os.environ.get("DEBUG", False)


def create_server() -> Flask:
    """
    Creates a server.

    :returns:   The Flask server
    :rtype:     Flask
    """
    server = Flask(__name__)
    server.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    server.config["UPLOAD_FOLDER"] = os.path.join(
        gettempdir(), "analyser"
    )
    if not os.path.exists(server.config["UPLOAD_FOLDER"]):
        os.makedirs(server.config["UPLOAD_FOLDER"])

    server.register_blueprint(main)

    return server


if __name__ == "__main__":
    server = create_server()
    server.run(host=HOST, port=PORT, debug=DEBUG)
