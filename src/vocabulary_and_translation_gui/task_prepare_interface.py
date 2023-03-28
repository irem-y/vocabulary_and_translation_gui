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
def task_check_dictionaires(depends_on, produces):
    if check_for_dictionaries(dictionaries_path=str(depends_on)):
        msg = "Success!\nAll dicts are available."
    else:
        msg = "Failure!\nNot all dicts are available."

    with open(produces, 'w') as f:
        f.write(msg)
