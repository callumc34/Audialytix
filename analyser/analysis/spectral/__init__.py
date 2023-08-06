from essentia import Pool, run
from essentia.streaming import *


def analyse(
    filename: str, frame_size: int = 1024, hop_size: int = 512
) -> Pool:
    loader = MonoLoader(filename=filename)
    frameCutter = FrameCutter(frameSize=frame_size, hopSize=hop_size)
    w = Windowing()
    spec = Spectrum()

    complexity = SpectralComplexity()

    pool = Pool()

    loader.audio >> frameCutter.signal
    frameCutter.frame >> w.frame >> spec.frame
    spec.spectrum >> complexity.spectrum

    complexity.spectralComplexity >> (pool, "complexity")

    run(loader)

    return pool
