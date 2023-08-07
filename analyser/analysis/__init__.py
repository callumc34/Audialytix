from .onset import OnsetAnalyser
from .spectral import SpectralAnalyser


def analyse_file(filename: str, options: dict) -> dict:
    """
    Analyse the given file.

    :param      options:  The options
    :type       options:  dict

    :returns:   The analysis results.
    :rtype:     dict
    """

    return {
        "onset": OnsetAnalyser(filename)()
        if options.get("onset")
        else None,
        "spectral": SpectralAnalyser(filename)()
        if options.get("spectral")
        else None,
    }


__all__ = ["onset", "spectral"]
