import pytest

from eed_webscrapping_scripts.modules import decode_string


@pytest.mark.parametrize(
    "encoded_string, expected_output",
    [
        ("Beifu\xc3\x9f", "Beifuß"),
        ("Gr\xc3\xa4ser", "Gräser"),
        ("M\xc3\xbcller", "Müller"),
        ("Sch\xc3\xb6n", "Schön"),
        ("Beifu\\xc3\\x9f", "Beifuß"),  # does not work
        ("Beifu\\xc3\\x9f".replace("\\\\", "\\"), "Beifuß"),  # does not work
        ("Beifu\\xc3\\x9f".replace("\\\\", "\\"), "Beifuß"),  # does not work
    ],
)
def test_decode_string(encoded_string, expected_output):
    assert decode_string(encoded_string) == expected_output
