from eed_webscrapping_scripts.modules import encrypt_direct

phrase = input("Enter the value you want to encrypt ")

encryptd_phrase = encrypt_direct(phrase)

print(f"{phrase=}")
print(f"{encryptd_phrase=}")
