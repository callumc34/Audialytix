from typing import Callable

from essentia import Pool, run
from essentia.streaming import AudioLoader, MonoLoader, StereoDemuxer, _StreamConnector


class _Runner:
    """
    This class describes an audio analysis runner.
    """

    def __init__(
        self,
        analyser: Callable,
        filename: str,
        frame_size: int = 1024,
        hop_size: int = 512,
    ):
        """
        Constructs a new instance.

        :param      analyser:    The analyser
        :type       analyser:    Callable
        :param      filename:    The filename
        :type       filename:    str
        :param      frame_size:  The frame size
        :type       frame_size:  int
        :param      hop_size:    The hop size
        :type       hop_size:    int
        """
        self._analyser = analyser

        self._filename = filename
        self._frame_size = frame_size
        self._hop_size = hop_size

        # To be implemented by runner type
        self._loader = None

        # To store results
        self._pool = Pool()

    def _configure(self):
        """
        Configure the streams for the analysis.
        """
        raise NotImplementedError("Runner must implement configure")

    def __call__(self) -> Pool:
        """
        Run the analysis.

        :returns:   Pools of the results
        :rtype:     Pool
        """
        run(self._loader)

        return self._pool


class MonoRunner(_Runner):
    """
    This class describes a runner that uses one audio channel.
    """

    def __init__(
        self,
        analyser: Callable,
        filename: str,
        frame_size: int = 1024,
        hop_size: int = 512,
    ):
        super().__init__(analyser, filename)

        self._loader = MonoLoader(filename=self._filename)

        self._configure()

    def _configure(self):
        self._analyser(
            self._loader.audio,
            self._pool,
            self._frame_size,
            self._hop_size,
        )


class StereoRunner(_Runner):
    """
    This class describes a stereo runner.
    """

    def __init__(
        self,
        analyser: Callable,
        filename: str,
        frame_size: int = 1024,
        hop_size: int = 512,
    ):
        super().__init__(analyser, filename)

        self._loader = AudioLoader(filename=self._filename)
        self._demuxer = StereoDemuxer()

        self._loader.audio >> self._demuxer.audio

        # Unused
        self._loader.sampleRate >> None
        self._loader.numberChannels >> None
        self._loader.md5 >> None
        self._loader.bit_rate >> None
        self._loader.codec >> None

        self._left_pool = Pool()
        self._right_pool = Pool()

        self._configure()

    def _configure(self):
        self._analyser(
            self._demuxer.left,
            self._left_pool,
            self._frame_size,
            self._hop_size,
        )
        self._analyser(
            self._demuxer.right,
            self._right_pool,
            self._frame_size,
            self._hop_size,
        )

    def __call__(self) -> Pool:
        run(self._loader)
        for key in self._left_pool.descriptorNames():
            self._pool.merge("left." + key, self._left_pool[key], "replace")

        for key in self._right_pool.descriptorNames():
            self._pool.merge("right." + key, self._right_pool[key], "replace")

        return self._pool
