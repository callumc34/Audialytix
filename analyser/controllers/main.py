from .threads import AnalyseThread

import os, os.path

from flask import (
    Blueprint,
    current_app,
    request,
    copy_current_request_context,
)
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

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

    else:
        if current_app.config["DEBUG"]:
            print(e)

    return "Internal server error.", 500


@main.route("/analyse", methods=["POST"])
def analyse():
    @copy_current_request_context
    def cleanup(result: dict, filename: str) -> None:
        with current_app.app_context():
            os.remove(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"], filename
                )
            )

    filename = secure_filename(request.files["file"].filename)
    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], filename
    )

    request.files["file"].save(file_path)

    options = {
        "onset": request.form.get("onset", False),
        "spectral": request.form.get("spectral", False),
    }

    results = AnalyseThread(
        file_path,
        options,
        lambda result: cleanup(result, filename),
    ).start()

    return "OK", 200


@main.route("/*")
def all():
    return "Not a valid route.", 400
