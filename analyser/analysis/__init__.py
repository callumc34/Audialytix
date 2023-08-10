from typing import Callable

from .onset import onset_analysis
from .runner import MonoRunner, StereoRunner
from .spectral import spectral_analysis


def _analyse_channels(
    channel_runner: Callable, analysis_runner: Callable, filename: str, **kwargs
) -> dict:
    """
    Run analysis for a given runner analysis and channels

    :param      channel_runner:   The channel runner
    :type       channel_runner:   Callable
    :param      analysis_runner:  The analysis runner
    :type       analysis_runner:  Callable
    :param      filename:         The filename
    :type       filename:         str
    :param      kwargs:           The keywords arguments
    :type       kwargs:           dictionary

    :returns:   Result of the analysis
    :rtype:     dict
    """
    return channel_runner(analysis_runner, filename, **kwargs)()


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
    result = {}
    channel_runner = StereoRunner if kwargs.get("stereo", False) else MonoRunner

    if "onset" in kwargs:
        result["onset"] = _analyse_channels(
            channel_runner, onset_analysis, filename, **kwargs["onset"]
        )

    if "spectral" in kwargs:
        result["spectral"] = _analyse_channels(
            channel_runner, spectral_analysis, filename, **kwargs["spectral"]
        )

    return result


__all__ = ["onset", "spectral"]
