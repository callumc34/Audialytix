import asyncio
import json
import os
import os.path


def cleanup_analysis(file_path: str, future: asyncio.Future) -> None:
    """
    Cleanup files generated by analysis.

    :param      file_path:  The file path
    :type       file_path:  str
    :param      future:     The future
    :type       future:     Result of the analysis task

    :returns:   Nothing
    :rtype:     None
    """
    os.remove(file_path)
    os.rmdir(os.path.dirname(file_path))


def parse_analysis_form(form: dict) -> dict:
    """
    Parse the specification of the analysis form.

    :param      form:  The form
    :type       form:  dict

    :returns:   The dictionary of the result
    :rtype:     dict
    """

    result = {}
    for key, value in form.items():
        try:
            result[key] = json.loads(value)
        except json.decoder.JSONDecodeError:
            result[key] = value

    return result