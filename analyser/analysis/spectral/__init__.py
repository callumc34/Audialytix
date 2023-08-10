from essentia import Pool
from essentia.streaming import (
    FFT,
    CartesianToPolar,
    FrameCutter,
    SpectralComplexity,
    Spectrum,
    Windowing,
    _StreamConnector,
)


def spectral_analysis(
    audio_source: _StreamConnector,
    pool: Pool,
    frame_size: int = 1024,
    hop_size: int = 512,
) -> None:
    """
    Perform spectral analysis on a file.

    :param      audio_source:  The audio source
    :type       audio_source:  _StreamConnector
    :param      pool:          The pool
    :type       pool:          Pool
    :param      frame_size:    The frame size
    :type       frame_size:    int
    :param      hop_size:      The hop size
    :type       hop_size:      int

    :returns:   Nothing
    :rtype:     None
    """
    frameCutter = FrameCutter(frameSize=frame_size, hopSize=hop_size)
    w = Windowing()
    spec = Spectrum()

    complexity = SpectralComplexity()

    audio_source >> frameCutter.signal
    frameCutter.frame >> w.frame >> spec.frame
    spec.spectrum >> complexity.spectrum

    complexity.spectralComplexity >> (pool, "complexity")
