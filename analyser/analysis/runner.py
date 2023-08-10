from essentia import Pool, run
from essentia.streaming import AudioLoader, StereoDemuxer, _StreamConnector


class _Runner:
    def __init__(self, filename: str, frame_size: int = 1024, hop_size: int = 512):
        self._filename = filename
        self._frame_size = frame_size
        self._hop_size = hop_size

        # To be implemented by runner type
        self._loader = None

        # To store results
        self._pool = Pool()

    def _configure(self):
        raise NotImplementedError("Runner must implement configure")

    def _analyse(
        self,
        audio_source: _StreamConnector,
        pool: Pool,
        frame_size: int = 1024,
        hop_size: int = 512,
    ) -> None:
        raise NotImplementedError("Runner must implement analyse")

    def __call__(self) -> Pool:
        run(self._loader)

        return self._pool


class MonoRunner(_Runner):
    def __init__(self, filename: str, frame_size: int = 1024, hop_size: int = 512):
        super().__init__(filename)

        self._loader = AudioLoader(filename=self._filename)

    def _configure(self):
        def wrapper(frame_size: int = 1024, hop_size: int = 512) -> None:
            self._analyse(
                self._loader.audio,
                self._pool,
                self._frame_size,
                self._hop_size,
            )

        return wrapper


class StereoRunner(_Runner):
    def __init__(self, filename: str, frame_size: int = 1024, hop_size: int = 512):
        super().__init__(filename)

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

    def _configure(self):
        self._analyse(
            self._demuxer.left,
            self._left_pool,
            self._frame_size,
            self._hop_size,
        )
        self._analyse(
            self._demuxer.right,
            self._right_pool,
            self._frame_size,
            self._hop_size,
        )

    def __call__(self) -> Pool:
        run(self._loader)

        for key in self._left_pool.descriptorNames():
            self._pool.add("left." + key, self._left_pool[key])

        for key in self._right_pool.descriptorNames():
            self._pool.add("right." + key, self._right_pool[key])

        return self._pool
