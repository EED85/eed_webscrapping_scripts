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
    result = cfg_test["encrytpion"]["result"]  # noqa
    phrase_decrypted = decrypt(result, generate_key(cfg_test["encrytpion"]["password"]))
    assert phrase_decrypted == phrase
