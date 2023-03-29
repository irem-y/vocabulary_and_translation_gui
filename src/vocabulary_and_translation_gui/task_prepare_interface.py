"""
Two task for  "check_for_dictionaries" and "get_deepl_key".

The tasks raises errors if they fail.
"""

import os
import pytask
from vocabulary_and_translation_gui.prepare_application import (
    get_deepl_key,
    check_for_dictionaries
)


@pytask.mark.depends_on(os.path.join(
        os.path.dirname(__file__), "resources", 'deepl_key.txt'
    )
)
def task_get_key(depends_on):
    """
    Check for a Key in depends_on.

    Raises an error if no key found.

    Args:
    - depends_on (path): Path of the DeepL Key file

    Returns:
    - None

    Raises:
    - RuntimeError: If no key found
    """
    if get_deepl_key(file_path=str(depends_on)) is False:
        raise RuntimeError("No Key found under: " + depends_on)


@pytask.mark.depends_on(os.path.join(
        os.path.dirname(__file__), "resources", "dictionaries"
    )
)
def task_check_dictionaries(depends_on):
    """
    Check if the dictionaries in depends_on are available in the enchant lib.

    Raise an error if a dictionary is missing.

    Args:
    - depends_on (path): Path of dictionaries

    Returns:
    - None

    Raises:
    - RuntimeError: If a dictionary is missing
    """
    if check_for_dictionaries(dictionaries_path=str(depends_on)) is not True:
        raise RuntimeError("Not all required dictionaries available.")
