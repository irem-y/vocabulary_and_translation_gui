"""
All functions for preparing the application.

Functions:
- check_for_dictionaries(dicts)
- get_deepl_key(file_path)
"""

import enchant
import os
from tkinter import messagebox


def check_for_dictionaries(dictionaries_path=""):
    """Check if needed dictionaries for enchantment exist.

    Args:
    - dictionaries_path (str): the path to the file with the names of the
    needed dictionaries

    Returns:
    - Boolean
    """
    # Check if dicts is a list
    if not isinstance(dictionaries_path, str):
        messagebox.showerror(title="wrong datatype",
                             message="'dictionaries_path has to be a string.")
        return

    # Check if there are values in dicts
    if len(dictionaries_path) <= 0:
        return False

    # Get the dictionaries from the file
    dictionary_list = []
    for dictionary in os.listdir(dictionaries_path):
        dictionary_list.append(dictionary.split('.')[0])

    dicts = list(dict.fromkeys(dictionary_list))

    # Create an empty list for the possible missing dictionary
    missing_dicts = []

    # Check for each dictionary in dicts, if it exist
    for dic in dicts:
        # If a dictionary not exist, add it to missing_dicts as .dic and .aff
        if not enchant.dict_exists(dic):
            missing_dicts.append(dic + ".dic")
            missing_dicts.append(dic + ".aff")

    # If missing dictionaries are found, find the correct destination path
    if len(missing_dicts) > 0:

        # Get the path of the available dictionaries
        dict_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "resources",
                                                 "dictionaries")
                                    )

        # Get the path of the relevant folder of the enchant library
        for entry in os.walk(os.path.dirname(enchant.__file__)):
            if r"share\enchant" in entry[0]:
                dest_path = entry[0]

        # Create title and message for the warning message
        titles = {
            "dic": "Add dictionaries to the enchant folder"
        }
        messages = {
            "dic": ("The following dictionaries:\n'"
                    + "', '".join(missing_dicts)
                    + "'\nhas to be added to\n" + dest_path
                    + "\n You can find the dictionaries here:\n"
                    + dict_path)
        }

        # Give the user a warning message, to show which dictionaries are
        # missing and where they have to be copied
        messagebox.showwarning(title=titles["dic"],
                               message=messages["dic"])

        return False

    else:
        return True


def get_deepl_key(file_path=""):
    """Find the DeepL Auth Key.

    Args:
    - file_path (str): Path of the file in which the DeepL key is

    Returns:
    - line (str): DeepL Auth Key
    """
    # Check if file_path is a string
    if not isinstance(file_path, str):
        messagebox.showerror(title="Wrong data type",
                             message="file_type hast to be a string")
        return False
    # Create titles and messages for the warning messages
    titles = {
        "key": "No Key found",
        "access": "No Access Permissions",
        "file": "No File found"
    }

    messages = {
        "key": "No Key found in File: " + file_path,
        "access": "No Access Permissions for the file: " + file_path,
        "file": "No File found under: " + file_path
    }
    # Check if file_path exist
    if os.path.exists(file_path):
        # Open the file and search for the key
        try:
            with open(file_path) as f:
                lines = f.readlines()
            for line in reversed(lines):
                # The last uncommented line will be returned
                if line[0] != "#":
                    return line

            # If no key is found, give the user a warning message
            messagebox.showwarning(title=titles["key"],
                                   message=messages["key"])
            return False
        # If there is a permission error, give the user a warning message
        except PermissionError:
            messagebox.showwarning(title=titles["access"],
                                   message=messages["access"])
            return False
    else:
        # If the file not exist, give the user a warning message
        messagebox.showwarning(title=titles["file"],
                               message=messages["file"])
        return False
