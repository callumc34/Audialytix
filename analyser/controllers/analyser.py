from analysis.onset import analyse
from analysis import analyse_file

import threading

from time import sleep
from typing import Callable


class AnalyseThread(threading.Thread):
    def __init__(
        self, filename: str, options: dict, callback: Callable
    ) -> None:
        super().__init__()
        self.daemon = True
        self._filename = filename
        self._options = options
        self._callback = callback

    def run(self) -> None:
        # Without sleep the threading doesn't actually work for some reason
        sleep(0.001)

        self._callback(analyse_file(self._filename, self._options))
