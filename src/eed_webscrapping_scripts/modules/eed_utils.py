import random
import time


def sleep(
    minimum_seconds: float = 0, maximum_seconds: float = 1, seed: int = None, ndigits: int = None
) -> float:
    """
    Pauses the program execution for a random duration between minimum_seconds and maximum_seconds.

    Parameters:
    minimum_seconds (float): The minimum number of seconds to sleep. Default is 0.
    maximum_seconds (float): The maximum number of seconds to sleep. Default is 1.
    seed (int, optional): A seed value for the random number generator. Default is None.

    Returns:
    float: The actual number of seconds the program slept.
    """
    if seed is not None:
        random.seed(seed)
    sleep_in_seconds = random.uniform(minimum_seconds, maximum_seconds)
    if ndigits is not None:
        sleep_in_seconds = round(sleep_in_seconds, ndigits)
    time.sleep(sleep_in_seconds)
    return sleep_in_seconds
