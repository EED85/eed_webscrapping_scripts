from eed_webscrapping_scripts.modules import decrypt, encrypt, generate_key

phrase = "123"


def test_encrypt_decrypt(cfg_test):
    """Test asymmetry."""
    key = generate_key(cfg_test["encrytpion"]["password"])
    phrase_encrypt = encrypt(phrase, key)
    phrase_decrypted = decrypt(phrase_encrypt, key)
    assert phrase_decrypted == phrase


def test_constant_decrypt(cfg_test):
    """Test constant decryption."""
    key = generate_key(cfg_test["encrytpion"]["password"])
    result = cfg_test["encrytpion"]["result"]
    phrase_decrypted = decrypt(result, key)
    assert phrase_decrypted == phrase
