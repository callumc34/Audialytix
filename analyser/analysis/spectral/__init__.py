from ..runner import StereoRunner

from essentia import Pool
from essentia.streaming import (
    CartesianToPolar,
    FFT,
    FrameCutter,
    Windowing,
    Spectrum,
    SpectralComplexity,
    _StreamConnector,
)


class SpectralAnalyser(StereoRunner):
    def __init__(
        self, filename: str, frame_size: int = 1024, hop_size: int = 512
    ):
        super().__init__(
            filename, frame_size=frame_size, hop_size=hop_size
        )

        self._configure()

    def _analyse(
        self,
        audio_source: _StreamConnector,
        pool: Pool,
        frame_size: int = 1024,
        hop_size: int = 512,
    ) -> None:
        frameCutter = FrameCutter(
            frameSize=frame_size, hopSize=hop_size
        )
        w = Windowing()
        spec = Spectrum()

        complexity = SpectralComplexity()

        audio_source >> frameCutter.signal
        frameCutter.frame >> w.frame >> spec.frame
        spec.spectrum >> complexity.spectrum

        complexity.spectralComplexity >> (pool, "complexity")
