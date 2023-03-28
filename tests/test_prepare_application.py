import os
import pytest
from vocabulary_and_translation_gui.prepare_application import (
    get_deepl_key,
    check_for_dictionaries
    )
from unittest.mock import patch


class TestGetDeeplKey:
    """
    Test cases for the "get_deepl_key" function.

    This class defines test methods to ensure the "get_deepl_key"
    function in the "prepare_application" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_invalid_file: Test the "get_deepl_key" function with not
        correct files.
        - test_valid_file: Test the "get_deepl_key" function with a file
        with a key.
    """
    @pytest.mark.parametrize("file_name", [
        ("abc.txt"),
        ("no_key.txt"),
    ])
    def test_invalid_file(self, file_name):
        """
        Test the "get_deepl_key" function with not correct files.

        The expected output is not True

        Args:
        - file_name (str): the name of the file where a key is stored

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(os.path.dirname(__file__), "test_files")
        file_path = os.path.join(path, file_name)
        with patch("tkinter.messagebox.showwarning", return_value=True):
            assert get_deepl_key(file_path=file_path) is not True

    def test_valid_file(self):
        """
        Test the "get_deepl_key" function with a file with a key.

        The expected output is a string

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(os.path.dirname(__file__), "test_files")
        file_path = os.path.join(path, "key.txt")
        assert type(get_deepl_key(file_path=file_path)) == str


class TestCheckForDictionaries:
    """
    Test cases for the "check_for_dictionaries" function.

    This class defines test methods to ensure the "check_for_dictionaries"
    function in the "prepare_application" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_existing_dicts: Test the "check_for_dictionaries" function for
        existing dicts.
        - test_non_existing: Test the "check_for_dictionaries" for not
        existing dicts.
    """

    def test_existing_dicts(self):
        """
        Test the "check_for_dictionaries" function for existing dicts.

        The expected output is True.

        Args:
        - None

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(os.path.dirname(__file__), "test_files",
                            "test_dicts_exist")
        assert check_for_dictionaries(dictionaries_path=path) is True

    def test_non_existing(self):
        """
        Test the "check_for_dictionaries" for not existing dicts.

        The expected output is False.

        Args:
        - None

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(os.path.dirname(__file__), "test_files",
                            "test_dicts_not_exist")
        with patch("tkinter.messagebox.showwarning", return_value=True):
            assert check_for_dictionaries(dictionaries_path=path) is not True
