from essentia import Pool
from essentia.streaming import (
    FFT,
    CartesianToPolar,
    FrameCutter,
    MonoLoader,
    OnsetDetection,
    Windowing,
    _StreamConnector,
)


def onset_analysis(
    audio_source: _StreamConnector,
    pool: Pool,
    frame_size: int = 1024,
    hop_size: int = 512,
) -> None:
    """
    Perform onset analysis on a file.

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

    w = Windowing(type="hann")
    fft = FFT()
    c2p = CartesianToPolar()

    od_hfc = OnsetDetection(method="hfc")
    od_complex = OnsetDetection(method="complex")

    # Connect the algorithms
    audio_source >> frameCutter.signal
    frameCutter.frame >> w.frame >> fft.frame
    fft.fft >> c2p.complex

    c2p.magnitude >> od_hfc.spectrum
    c2p.phase >> od_hfc.phase
    c2p.magnitude >> od_complex.spectrum
    c2p.phase >> od_complex.phase

    od_hfc.onsetDetection >> (pool, "od.hfc")
    od_complex.onsetDetection >> (pool, "od.complex")
