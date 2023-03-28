"""
Two task for  "check_for_dictionaries" and "get_deepl_key".

The tasks produce output files to document the success or failure of the
checks.
"""

from vocabulary_and_translation_gui.config import BLD
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
@pytask.mark.produces(BLD / "key_check_result.txt")
def task_get_key(depends_on, produces):
    """
    Check for a Key in depends_on.

    A text file in produces gets created, which checks if a Key was found or
    not.

    Args:
    - depends_on (path): Path of the DeepL Key file
    - produces (path): Path for the output file

    Returns:
    - None
    """
    if get_deepl_key(file_path=str(depends_on)):
        msg = ("Success!\nA DeepL authentication key is available here:\n"
               + str(depends_on))
    else:
        msg = ("Failure!\nNo DeepL authentication key is available here:\n"
               + str(depends_on))

    with open(produces, 'w') as f:
        f.write(msg)


@pytask.mark.depends_on(os.path.join(
        os.path.dirname(__file__), "resources", "dictionaries"
    )
)
@pytask.mark.produces(BLD / "dicts_check_result.txt")
def task_check_dictionaries(depends_on, produces):
    """
    Check if the dictionaries in depends_on are available in the enchant lib.

    A text file in produces gets created, which checks if all dictionaries
    were found or not.

    Args:
    - depends_on (path): Path of dictionaries
    - produces (path): Path for the output file

    Returns:
    - None
    """
    if check_for_dictionaries(dictionaries_path=str(depends_on)):
        msg = "Success!\nAll dicts are available."
    else:
        msg = "Failure!\nNot all dicts are available."

    with open(produces, 'w') as f:
        f.write(msg)
