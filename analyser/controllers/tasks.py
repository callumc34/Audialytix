from analysis import analyse_file

import asyncio

from typing import Callable


async def analyse_task(file_path: str, options: dict) -> dict:
    # Return control to the event loop.
    await asyncio.sleep(0.01)
    return analyse_file(file_path, options)
