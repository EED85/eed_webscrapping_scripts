import random
import time


def sleep_random(
    minimum_seconds: float = 0, maximum_seconds: float = 1, seed: int = None, ndigits: int = None
) -> float:
    """
    Pauses the program execution for a random duration between minimum_seconds and maximum_seconds.

    Parameters:
    minimum_seconds (float): The minimum number of seconds to sleep_random. Default is 0.
    maximum_seconds (float): The maximum number of seconds to sleep_random. Default is 1.
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


def decode_string(encoded_string: str, encode: str = "latin1", decode: str = "utf-8") -> str:
    """
    Decodes an encoded string from Latin-1 to UTF-8.

    Parameters:
    encoded_string (str): The encoded string to decode.

    Returns:
    str: The decoded string.
    """
    return encoded_string.encode(encode).decode(decode)
