from eed_webscrapping_scripts.modules import decrypt, encrypt, generate_key

phrase = "123"


def test_encrypt_decrypt(cfg_test):
    phrase_encrypt = encrypt(phrase, generate_key(cfg_test["encrytpion"]["password"]))
    phrase_decrypted = decrypt(phrase_encrypt, generate_key(cfg_test["encrytpion"]["password"]))
    assert phrase_decrypted == phrase


# lokal durchführen - hier klappt es. Warum es nicht in den Github Actions nicht klappt
#  ist mir vollkommen unklar
def test_constant_decrypt(cfg_test):
    """Test constant decryption."""
    result = b"""gAAAAABn4bJ7yHdIjULRgRui9pm65cYEJF8Wzd5O58xrPLQ0YaoUGt_lwwovlmuQJkjkqjBAxicScsBIp_EWHzKFQ0X1oXaKNQ=="""  # noqa
    phrase_decrypted = decrypt(result, generate_key(cfg_test["encrytpion"]["password"]))
    assert phrase_decrypted == phrase
