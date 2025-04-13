import pytest

from eed_webscrapping_scripts.modules import sleep_random


@pytest.mark.parametrize(
    "minimum_seconds, maximum_seconds, seed, minimum_seconds_expected, maximum_seconds_expected",
    [
        (0, 0.0001, None, 0, 0.0001),
        (0, 0.01, 42, 0.006394267984578837, 0.006394267984578837),
    ],
    ids=[
        "without seed",
        "with seed",
    ],
)
def test_sleep(
    minimum_seconds, maximum_seconds, seed, minimum_seconds_expected, maximum_seconds_expected
):
    result = sleep_random(minimum_seconds, maximum_seconds, seed)
    assert minimum_seconds_expected <= result <= maximum_seconds_expected
