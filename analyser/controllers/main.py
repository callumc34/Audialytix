import asyncio
import os
import os.path
import uuid
from functools import partial

from flask import Blueprint, copy_current_request_context, current_app, request
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from .tasks import analyse_task

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


def cleanup(file_path: str, future: asyncio.Future) -> None:
    os.remove(file_path)
    os.rmdir(os.path.dirname(file_path))


@main.route("/analyse", methods=["POST"])
async def analyse():
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], str(uuid.uuid4().hex))
    filename = secure_filename(request.files["file"].filename)
    file_path = os.path.join(folder, filename)

    os.mkdir(folder)
    request.files["file"].save(file_path)

    options = {
        "onset": request.form.get("onset", "False").casefold() in ("true", "1", "on"),
        "spectral": request.form.get("spectral", "False").casefold()
        in ("true", "1", "on"),
    }

    task = asyncio.create_task(analyse_task(file_path, options))
    task.add_done_callback(partial(cleanup, file_path))

    return "OK", 200


@main.route("/alive")
def alive():
    return "OK", 200


@main.route("/*")
def all():
    return "Not a valid route.", 400
