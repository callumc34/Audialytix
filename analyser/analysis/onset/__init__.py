from essentia import Pool, run
from essentia.streaming import (
    MonoLoader,
    FrameCutter,
    OnsetDetection,
    Windowing,
    FFT,
    CartesianToPolar,
)


def analyse(
    filename: str, frame_size: int = 1024, hop_size: int = 512
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
    :rtype:     Pool
    """
    loader = MonoLoader(filename=filename)
    frameCutter = FrameCutter(frameSize=frame_size, hopSize=hop_size)

    w = Windowing(type="hann")
    fft = FFT()
    c2p = CartesianToPolar()

    od_hfc = OnsetDetection(method="hfc")
    od_complex = OnsetDetection(method="complex")

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
