"""
All functions for preparing the application.

Functions:
- check_for_dictionaries(dicts)
- get_deepl_key(fiel_path)
"""

import enchant
import os
from tkinter import messagebox


def check_for_dictionaries(dicts=[]):
    """Check if needed dictionarys for enchantment exist.

    Args:
    - dicts (list): List of the dictionary tags

    Returns:
    - Boolean
    """
    # Check if dicts is a list
    if not isinstance(dicts, list):
        messagebox.showerror(title="wrong datatype",
                             message="'dictsÄ has to be a list.")
        return

    # Check if there are values in dicts
    if len(dicts) <= 0:
        return False
    # Create an empty list for the possible missing dictionary
    missing_dicts = []

    # Check for each dictionary in dicts, if it exist
    for dic in dicts:
        # If a dictionary not exist, add it to missing_dicts as .dic and .aff
        if not enchant.dict_exists(dic):
            missing_dicts.append(dic + ".dic")
            missing_dicts.append(dic + ".aff")

    # If missing dictionaries are found, find the corerect destination path
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
            "dic": "Add dictionarys to the enchant folder"
        }
        messages = {
            "dic": ("The following dictionarys:\n'"
                    + "', '".join(missing_dicts)
                    + "'\nhas to be added to\n" + dest_path
                    + "\n You can find the dictionaries here:\n"
                    + dict_path)
        }

        # Give the user a warning message, to show which dictionarys are
        # missing and where they have to be copied
        messagebox.showwarning(title=titles["dic"],
                               message=messages["dic"])

        return False

    else:
        return True


def get_deepl_key(file_path=""):
    """Find the Deepl Auth Key.

    Args:
    - file_path (str): Path of the file in which the deepl key is

    Returns:
    - line (str): Deepl Auth Key
    """
    # Check if file_path is astring
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
        "access": "No Access Permmsions for the file: " + file_path,
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
