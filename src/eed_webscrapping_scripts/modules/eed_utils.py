import functools
import pathlib
import random
import time


def sleep_random(
    minimum_seconds: float = 0, maximum_seconds: float = 1, seed: int = None, ndigits: int = None
) -> float:
    """
    Pauses the program execution for a random duration between minimum_seconds and maximum_seconds.

    Parameters
    ----------
    minimum_seconds : float, optional
        The minimum number of seconds to sleep. Default is 0.
    maximum_seconds : float, optional
        The maximum number of seconds to sleep. Default is 1.
    seed : int, optional
        A seed value for the random number generator. Default is None.
    ndigits : int, optional
        The number of decimal places to round the sleep duration to. Default is None.

    Returns
    -------
    float
        The actual number of seconds the program slept.
    """
    if seed is not None:
        random.seed(seed)
    sleep_in_seconds = random.uniform(minimum_seconds, maximum_seconds)
    if ndigits is not None:
        sleep_in_seconds = round(sleep_in_seconds, ndigits)
    time.sleep(sleep_in_seconds)
    return sleep_in_seconds


# ---------------------------------------------
# os utils
# ---------------------------------------------


@functools.singledispatch
def file_exists(file_path) -> bool:
    """
    Check if a file exists at the given path.

    Parameters
    ----------
    file_path : str | pathlib.PosixPath | pathlib.WindowsPath
        The path to the file.

    Returns
    -------
    bool
        True if the file exists, False otherwise.
    """
    raise NotImplementedError(f"Unsupported type: {type(file_path)}")


@file_exists.register(str)
def _(file_path: str) -> bool:
    return pathlib.Path(file_path).is_file()


@file_exists.register(pathlib.PosixPath)
@file_exists.register(pathlib.WindowsPath)
def _(file_path: pathlib.WindowsPath | pathlib.PosixPath) -> bool:
    return file_path.is_file()
