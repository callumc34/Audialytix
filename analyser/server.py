#!/usr/bin/env python
import os

from dotenv import load_dotenv
from flask import Flask

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
    server.register_blueprint(main)
    return server


if __name__ == "__main__":
    server = create_server()
    server.run(host=HOST, port=PORT, debug=DEBUG)
