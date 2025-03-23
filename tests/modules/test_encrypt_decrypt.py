from eed_webscrapping_scripts.modules import decrypt, encrypt

phrase = "123"


def test_encrypt_decrypt(cfg_test):
    """Test asymmetry."""
    key = cfg_test["encrytpion"]["key"]
    phrase_encrypt = encrypt(phrase, key)
    phrase_decrypted = decrypt(phrase_encrypt, key)
    assert phrase_decrypted == phrase


def test_constant_decrypt(cfg_test):
    """Test constant decryption."""
    key = cfg_test["encrytpion"]["key"]
    result = cfg_test["encrytpion"]["result"]
    phrase_decrypted = decrypt(result, key)
    assert phrase_decrypted == phrase
