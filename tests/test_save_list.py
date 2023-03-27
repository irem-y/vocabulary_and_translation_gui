import datetime
import os
import pandas as pd
import pytest
from src.vocabulary_and_translation_gui.save_list import (
    save_list_as_apkg,
    save_list_as_xlsx
)
from unittest.mock import patch


class TestSaveListAsApkg:
    """
    Test cases for the "save_list_as_apkg" function.

    This class defines test methods to ensure the "save_list_as_apkg"
    function in the "save_list" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_wrong_list: Test the "save_list_as_apkg" function for an wrong
        input list.
        - test_creating_file: Test the "save_list_as_apkg" function with valid
        inputs to create a file.
    """
    @pytest.mark.parametrize("word_list", [
        ([['apple', 'Apfel', datetime.datetime.now()]]),
        ([['book', 'Buch', 'kitap', datetime.datetime.now()],
          ['computer', 'wrong', 'Computer', 'bilgisayar',
           datetime.datetime.now()]]),
        ([]),
    ])
    def test_wrong_list(self, tmp_path, word_list):
        """
        Test the "save_list_as_apkg" function for an wrong input list.

        The expected output is that None get returned when one or more of the
        lists inside word_list has an length unequal 4.

        Args:
        - tmp_path (pathlib.WindowsPath): the temporary path to save the file
        - word_list (list): the input list consisting of three strings and a
        timestamp

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(tmp_path, 'test.apkg')
        with patch("tkinter.messagebox.showwarning", return_value=True):
            save_list_as_apkg(word_list=word_list, path=path)
            assert os.path.exists(path=path) is not True

    @pytest.mark.parametrize("word_list", [
        ([['apple', 'Apfel', 'elma', datetime.datetime.now()]]),
        ([['book', 'Buch', 'kitap', datetime.datetime.now()],
          ['computer', 'Computer', 'bilgisayar', datetime.datetime.now()]]),
    ])
    def test_creating_file(self, tmp_path, word_list):
        """
        Test the "save_list_as_apkg" function with valid inputs.

        The expected output is that a file gets created.

        Args:
        - tmp_path (pathlib.WindowsPath): the temporary path to save the file
        - word_list (list): the input list consisting of three strings and a
        timestamp

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(tmp_path, 'test.apkg')
        with patch("tkinter.messagebox.showinfo", return_value=True):
            save_list_as_apkg(word_list=word_list, path=path)
            assert os.path.exists(path=path)


class TestSaveListAsXlsx:
    """
    Test cases for the "save_list_as_xlsx" function.

    This class defines test methods to ensure the "save_list_as_xlsx"
    function in the "save_list" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_empty_list:  Test the "save_list_as_xlsx" function for an empty
        input list.
        - test_creating_file: Test the "save_list_as_xlsx" function with valid
        inputs to create a file.
        - test_appending_file: Test the "save_list_as_xlsx" function with
        valid inputs to append a file.
    """

    @pytest.mark.parametrize("word_list", [
        ([['apple', 'Apfel', datetime.datetime.now()]]),
        ([['book', 'Buch', 'kitap', datetime.datetime.now()],
          ['computer', 'wrong', 'Computer', 'bilgisayar',
           datetime.datetime.now()]]),
        ([]),
    ])
    def test_wrong_list(self, tmp_path, word_list):
        """
        Test the "save_list_as_xlsx" function for an wrong input list.

        The expected output is that None get returned when one or more of the
        lists inside word_list has an length unequal 4.

        Args:
        - tmp_path (pathlib.WindowsPath): the temporary path to save the file
        - word_list (list): the input list consisting of three strings and a
        timestamp

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(tmp_path, 'test.xlsx')
        with patch("tkinter.messagebox.showwarning", return_value=True):
            save_list_as_xlsx(word_list=word_list, path=path)
            assert os.path.exists(path=path) is not True

    @pytest.mark.parametrize("word_list", [
        ([['apple', 'Apfel', 'elma', datetime.datetime.now()]]),
        ([['book', 'Buch', 'kitap', datetime.datetime.now()],
          ['computer', 'Computer', 'bilgisayar', datetime.datetime.now()]]),
    ])
    def test_creating_file(self, tmp_path, word_list):
        """
        Test the "save_list_as_xlsx" function with valid inputs.

        The expected output is that a file gets created.

        Args:
        - tmp_path (pathlib.WindowsPath): the temporary path to save the file
        - word_list (list): the input list consisting of three strings and a
        timestamp

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(tmp_path, 'test.xlsx')
        with patch("tkinter.messagebox.showinfo", return_value=True):
            save_list_as_xlsx(word_list=word_list, path=path)
            assert os.path.exists(path=path) is True

    @pytest.mark.parametrize("word_list, expected_len", [
        ([['apple', 'Apfel', 'elma', datetime.datetime.now()]], 2),
        ([['book', 'Buch', 'kitap', datetime.datetime.now()],
          ['computer', 'Computer', 'bilgisayar', datetime.datetime.now()]], 3),
    ])
    def test_appending_file(self, tmp_path, word_list, expected_len):
        """
        Test the "save_list_as_xlsx" function to append a file.

        The expected output is that the files get appended and has the length
        of the number of entries.

        Args:
        - tmp_path (pathlib.WindowsPath): the temporary path to save the file
        - word_list (list): the input list consisting of three strings and a
        timestamp
        - expected_len (int): The expected number of entrys of the file

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        path = os.path.join(tmp_path, 'test.xlsx')
        with patch("tkinter.messagebox.showinfo", return_value=True):
            save_list_as_xlsx(word_list=[['apple', 'Apfel', 'elma',
                                          datetime.datetime.now()]], path=path)
            assert os.path.exists(path=path) is True
            save_list_as_xlsx(word_list=word_list, path=path)
            df = pd.read_excel(path, sheet_name='Vocabulary')
            assert len(df) == expected_len
