import asyncio
import os
import os.path
import uuid
from functools import partial

from flask import Blueprint, current_app, request
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from .tasks import analyse_task
from .utils import cleanup_analysis, parse_analysis_form, return_results

main = Blueprint("main", __name__)


@main.errorhandler(Exception)
async def handle_exception(e: Exception) -> tuple:
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
async def analyse() -> tuple:
    """
    Request handler for analysing a posted file

    :returns:   HttpResponse OK
    :rtype:     tuple
    """

    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], str(uuid.uuid4().hex))
    filename = secure_filename(request.files["file"].filename)
    file_path = os.path.join(folder, filename)

    os.makedirs(folder, exist_ok=True)
    request.files["file"].save(file_path)

    options = parse_analysis_form(request.form.to_dict())

    task = asyncio.create_task(analyse_task(file_path, options))
    task.add_done_callback(partial(cleanup_analysis, file_path))
    task.add_done_callback(partial(return_results, options["webhook"]))

    return "OK", 200


@main.route("/alive")
def alive() -> tuple:
    """
    Health check for the server.

    :returns:   HttpResponse alive
    :rtype:     tuple
    """
    return "OK", 200


@main.route("/*")
def all() -> tuple:
    """
    Catch all route.

    :returns:   HttpResponse not valid route
    :rtype:     tuple
    """
    return "Not a valid route.", 400
