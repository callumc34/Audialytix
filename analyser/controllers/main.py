from flask import Blueprint
from werkzeug.exceptions import HTTPException

main = Blueprint("main", __name__)


@main.errorhandler(Exception)
def handle_exception(e: Exception) -> tuple:
    """
    Handles all exceptions thrown by the application.

    :param      e:    The exception
    :type       e:    Exception

    :returns:   The error message and the error code.
    :rtype:     tuple
    """
    if isinstance(e, HTTPException):
        return e

    return "Internal server error.", 500


@main.route("/analyse", methods=["POST"])
def analyse():
    return "wow"


@main.route("/*")
def all():
    return "Not a valid route.", 400
