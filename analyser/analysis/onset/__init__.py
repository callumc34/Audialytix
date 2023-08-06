from essentia import Pool, run
from essentia.streaming import *


def analyse(
    file: str, frameSize: int = 1024, hopSize: int = 512
) -> Pool:
    """
    Perform onset detection on the file and return the results in a pool.

    :param      file:       The file
    :type       file:       str
    :param      frameSize:  The frame size
    :type       frameSize:  int
    :param      hopSize:    The hop size
    :type       hopSize:    int

    :returns:   Pool of the onset detection values.
    :rtype:     essentia.Pool
    """
    loader = MonoLoader(filename=file)
    frameCutter = FrameCutter(frameSize=frameSize, hopSize=hopSize)

    od_hfc = OnsetDetection(method="hfc")
    od_complex = OnsetDetection(method="complex")

    w = Windowing(type="hann")
    fft = FFT()
    c2p = CartesianToPolar()

    pool = Pool()

    # Connect the algorithms

    loader.audio >> frameCutter.signal
    frameCutter.frame >> w.frame >> fft.frame
    fft.fft >> c2p.complex

    c2p.magnitude >> od_hfc.spectrum
    c2p.phase >> od_hfc.phase
    c2p.magnitude >> od_complex.spectrum
    c2p.phase >> od_complex.phase

    od_hfc.onsetDetection >> (pool, "od.hfc")
    od_complex.onsetDetection >> (pool, "od.complex")

    run(loader)

    return pool
