import pytest

from eed_webscrapping_scripts.modules import decode_string


@pytest.mark.parametrize(
    "encoded_string, expected_output",
    [
        ("Beifu\xc3\x9f", "Beifuß"),
        ("Gr\xc3\xa4ser", "Gräser"),
        ("M\xc3\xbcller", "Müller"),
        ("Sch\xc3\xb6n", "Schön"),
        # does only work with manually replacing
        ("Beifu\\xc3\\x9f", "Beifuß"),
        ("Gr\\xc3\\xa4ser", "Gräser"),
        # missing: ü, ö and probably more
    ],
)
def test_decode_string(encoded_string, expected_output):
    decoded_string = decode_string(encoded_string)
    assert decoded_string == expected_output
