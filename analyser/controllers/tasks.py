import asyncio

import requests
from analysis import analyse_file
from analysis.utils import pool_to_dict


async def analyse_task(file_path: str, options: dict) -> dict:
    """
    Analyse file task for the analyser application.

    :param      file_path:  The file path
    :type       file_path:  str
    :param      options:    The options with which to analyse.
    :type       options:    dict

    :returns:   Result of the analysis
    :rtype:     dict
    """

    # Return control to the event loop for other async functions to run
    await asyncio.sleep(0.01)

    return analyse_file(file_path, **options)


def return_results(webhook_options: dict, future: asyncio.Future) -> None:
    """
    Returns results to a webhook.

    :param      webhook_options:    The webhook options
    :type       webhook_options:    dict
    :param      future:             The future
    :type       future:             Result of the analysis task

    :returns:   Nothing
    :rtype:     None
    """

    url = webhook_options["webhook"]
    id = webhook_options["id"]
    response = future.result()

    json = {"id": id}
    for key in response:
        json[key] = pool_to_dict(response[key])

    requests.post(url, json=json)
