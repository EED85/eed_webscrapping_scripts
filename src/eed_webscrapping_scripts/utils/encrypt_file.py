from pathlib import Path

from eed_webscrapping_scripts.modules import encrypt_file

print(f"{Path.cwd()=}")
outfile = Path.cwd() / "encrypted_website.html"
file_path = input(
    r"Enter the path to the file to be enncrypted - without quotes and one Backslash (e.g. C:\test.txt):"
)

encrypt_file(file_path, outfile)
print(str(outfile))
