import asyncio

from analysis import analyse_file


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
