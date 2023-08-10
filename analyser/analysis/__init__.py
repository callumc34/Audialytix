from .onset import OnsetAnalyser
from .spectral import SpectralAnalyser


def analyse_file(filename: str, **kwargs) -> dict:
    """
    Analyse the given file and return the results as a dictionary.

    :param      filename:  The filename
    :type       filename:  str
    :param      kwargs:    The algorithms to analyse with
    :type       kwargs:    dictionary

    :returns:   The result of the analysis
    :rtype:     dict
    """

    return {
        "onset": OnsetAnalyser(filename)() if kwargs.get("onset") else None,
        "spectral": SpectralAnalyser(filename)() if kwargs.get("spectral") else None,
    }


__all__ = ["onset", "spectral"]
