"""
Running the application.

For the variable "key_path" add the path to your txt file, in which your
Deepl Key is safed.
"""

from interface_function import vocabulary_interface
from prepare_functions import (
    check_for_dicts,
    check_for_deepl_key
)

if __name__ == '__main__':
    # Path to Deepl Key file
    key_path = r"C:\Users\Irem\Desktop\Irem_Final_project\DeeplKey.txt"

    # Get a Deepl Key form key_path file, if possible
    deepl_auth_key = check_for_deepl_key(file_path=key_path)

    # Needed Dictionarys
    dictionarys = [
        "tr_TR",
        "de_DE",
        "en_GB"
    ]

    # Open the user interface if the needed dictioanrys and a Deepl Key could
    # be found
    if check_for_dicts(dictionarys) and deepl_auth_key:
        vocabulary_interface(deepl_auth_key)
