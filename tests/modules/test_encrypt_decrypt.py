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
    result = b"gAAAAABn4bShRo1HbvZ6GGd7-6V-SQOj-xdAXVTc-XxqMBAT0fPTnlUxCs264gb89-Al6HnOKNqUIQS4qBZ9gNnsdQS8OKHlGQ=="  # noqa
    phrase_decrypted = decrypt(result, generate_key(cfg_test["encrytpion"]["password"]))
    assert phrase_decrypted == phrase
