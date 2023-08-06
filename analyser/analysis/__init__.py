from . import onset, spectral


def analyse_file(filename: str, options: dict) -> dict:
    """
    Analyse the given file.

    :param      options:  The options
    :type       options:  dict

    :returns:   The analysis results.
    :rtype:     dict
    """

    return {
        "onset": onset.analyse(filename)
        if options.get("onset")
        else None,
        "spectral": spectral.analyse(filename)
        if options.get("spectral")
        else None,
    }


__all__ = ["onset", "spectral"]
