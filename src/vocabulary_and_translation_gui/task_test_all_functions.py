"""
A task to execute pytest for all test functions in the folder "tests".

The dependencies are the test files and the files with the functions that are
tested. If a new function or test function is created, add the file name here.
"""

import os
import pytask
import pytest

# Path and name of functions that are tested
function_path = os.path.dirname(__file__)
function_names = [
    "interface_and_features.py",
    "prepare_application.py",
    "save_list.py",
    "translation_and_spelling.py"
]

# Path and name of test functions
test_path = os.path.join(function_path, "..", "..", "tests")
test_names = [
    "test_import.py",
    "test_interface_and_features.py",
    "test_prepare_application.py",
    "test_save_list.py",
    "test_translation_and_spelling.py"
]

# List of all dependencies
dependencies = []
for function in function_names:
    dependencies.append(os.path.join(function_path, function))
for test_function in test_names:
    dependencies.append(os.path.join(test_path, test_function))


@pytask.mark.depends_on(dependencies)
def task_test_all_functions():
    """
    Run pytest for all tests files in vocabulary_and _translating_gui/tests.

    Args:
    - None

    Returns:
    - None
    """
    dirname = os.path.dirname(__file__)
    full_dir_name = os.path.abspath(os.path.join(dirname, "..", "..", "tests"))
    pytest.main([full_dir_name])
