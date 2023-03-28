"""
Running the application.

For the variable "key_path" add the path to your txt file, in which your
Deepl Key is safed.
"""

from vocabulary_and_translation_gui.interface_and_features import (
    vocabulary_interface
    )
import os
from vocabulary_and_translation_gui.prepare_application import (
    check_for_dictionaries,
    get_deepl_key
)

if __name__ == '__main__':
    # Path to Deepl Key file
    dirname = os.path.dirname(__file__)
    key_path = os.path.join(dirname, 'DeeplKey.txt')

    # Get a Deepl Key form key_path file, if possible
    deepl_auth_key = get_deepl_key(file_path=key_path)

    # Needed Dictionarys
    dictionarys = [
        "tr_TR",
        "de_DE",
        "en_GB"
    ]

    # Open the user interface if the needed dictioanrys and a Deepl Key could
    # be found
    if check_for_dictionaries(dictionarys) and deepl_auth_key:
        vocabulary_interface(deepl_auth_key)
