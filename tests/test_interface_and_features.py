import datetime
import os
import pytest
from src.vocabulary_and_translation_gui.interface_and_features import (
    handle_add_to_list,
    handle_save,
    handle_translate,
    vocabulary_interface
)
import tkinter as tk
from unittest.mock import patch


class TestHandleAddToList:
    """
    Test cases for the "handle_add_to_list" function.

    This class defines test methods to ensure the "handle_add_to_list"
    function in the "interface_and_features" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_valid_inputs: Test the "handle_add_to_list" function with valid
        inputs.
        - test_invalid_inputs: Test the "handle_add_to_list" function with
        invalid inputs.
    """
    @pytest.mark.parametrize(("in_text, src_lang, expected, expected_len,"
                              + "trans_list"), [
        ("der Baum ist groß", "Deutsch", "the tree is big", 1, []),
        ("the apple tastes good", "English", "the apple tastes good", 2,
         [["car", "Auto", "araba", datetime.datetime.now()]]),
        ("Çiçek güzel kokuyor", "Türkçe", "The flower smells good", 3,
         [["car", "Auto", "araba", datetime.datetime.now()],
          ["apple", "Apfel", "elma", datetime.datetime.now()]]),
    ])
    def test_valid_inputs(self, auth_key, in_text, src_lang, expected,
                          expected_len, trans_list):
        """
        Test the "handle_add_to_list" function with valid inputs.

        The expected ouptut is the input text with its translations added as a
        list to the trans_list

        Args:
        - auth_key (str): the key for the Deepl API
        - in_text (str): the word to check and correct
        - src_lang (str): the language of the expression
        - expected (str): the expected output for the given input
        - expected_len (int): expected length of the trans_list
        - trans_list (list[list]): the current wordlist

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        output = handle_add_to_list(key=auth_key, in_text=in_text,
                                    src_lang=src_lang, enter_field=tk.Entry(),
                                    translation_field=tk.Label(),
                                    trans_list_field=tk.Label(),
                                    trans_list=trans_list)
        assert len(output) == expected_len
        for word_list in output:
            assert len(word_list) == 4
        assert output[expected_len-1][0] == expected

    @pytest.mark.parametrize(("in_text, src_lang, enter_field,"
                              + "translation_field, trans_list"), [
        (123, "Deutsch", tk.Entry(), tk.Label(), []),
        ("der Baum ist groß", 123, tk.Entry(), tk.Label(), []),
        ("der Baum ist groß", "Deutsch", 123, tk.Label(), []),
        ("der Baum ist groß", "Deutsch", tk.Entry(), 123, []),
        ("der Baum ist groß", "Deutsch", tk.Entry(), tk.Label(), 123),
    ])
    def test_invalid_inputs(self, auth_key, in_text, src_lang, enter_field,
                            translation_field, trans_list):
        """
        Test the "handle_add_to_list" function with invalid inputs.

        The expected ouptut None

        Args:
        - auth_key (str): the key for the Deepl API
        - in_text (str): the word to check and correct
        - src_lang (str): the language of the expression
        - expected (str): the expected output for the given input
        - expected_len (int): expected length of the trans_list
        - trans_list (list[list]): the current wordlist

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.showerror", return_value=True):
            assert handle_add_to_list(key=auth_key, in_text=in_text,
                                      src_lang=src_lang,
                                      enter_field=enter_field,
                                      translation_field=translation_field,
                                      trans_list_field=tk.Label(),
                                      trans_list=trans_list) is None


class TestHandleSave:
    """
    Test cases for the "handle_save" function.

    This class defines test methods to ensure the "handle_save"
    function in the "interface_and_features" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_empty_list: Test the "handle_save" function for an empty input
        list.
        - test_no_path: Test the "handle_save" function if no path gets
        selected.
        - test_save_file: Test the "handle_save" function to the safe the list
        as file.
    """
    def test_empty_list(self):
        """
        Test the "handle_save" function for an empty input list.

        The expected output is that None get returned

        Args:
        - None

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.showwarning", return_value=True):
            assert handle_save(vocabulary_list=[]) is None

    def test_no_path(self):
        """
        Test the "handle_save" function if no path gets selected.

        The expected output is that None get returned, if the user don't
        enter a path and selects "no" in the retry messagebox.

        Args:
        - None

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.showinfo", return_value=True):
            with patch("tkinter.filedialog.asksaveasfilename",
                       return_value=""):
                with patch("tkinter.messagebox.askretrycancel",
                           return_value=False):
                    assert handle_save(vocabulary_list=[
                        ['apple', 'Apfel', 'elma', datetime.datetime.now()]
                        ]) is None

    @pytest.mark.parametrize("word_list", [
        ([['apple', 'Apfel', 'elma', datetime.datetime.now()]]),
        ([['book', 'Buch', 'kitap', datetime.datetime.now()],
          ['computer', 'Computer', 'bilgisayar', datetime.datetime.now()]]),
    ])
    def test_save_file(self, tmp_path, word_list):
        """
        Test the "handle_save" function to the safe the list as file.

        The expected output is that an file get created.

        Args:
        - tmp_path (pathlib.WindowsPath): the temporary path to save the file
        - word_list (list): the input list consisting of three strings and a
        timestamp

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.showinfo", return_value=True):
            with patch("tkinter.filedialog.asksaveasfilename",
                       return_value=os.path.join(tmp_path, 'test.xlsx')):
                handle_save(vocabulary_list=word_list)
                assert os.path.exists(os.path.join(tmp_path,
                                                   'test.xlsx')) is True

            with patch("tkinter.filedialog.asksaveasfilename",
                       return_value=os.path.join(tmp_path, 'test.apkg')):
                handle_save(vocabulary_list=word_list)
                assert os.path.exists(os.path.join(tmp_path,
                                                   'test.apkg')) is True


class TestHandleTranslate:
    """
    Test cases for the "handle_translate" function.

    This class defines test methods to ensure the "handle_translate"
    function in the "interface_and_features" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_valid_inputs: Test the "handle_translate" function with valid
        inputs.
        - test_invalid_inputs:  Test the "handle_translate" function with
        invalid inputs.
        - test_empty_text: Test the "handle_translate" function with an empty
        text.
        - test_wrong_text: Test the "handle_translate" function with incorrect
        written text.
    """
    @pytest.mark.parametrize("in_text, src_lang, tgt_lang, expected", [
        ("Baum", "Deutsch", "English", "Source language: DE\nEnglish: Tree"),
        ("Fernseher", "Deutsch", "Türkçe",
         "Source language: DE\nTürkçe: Televizyon"),
        ("Televizyon", "Türkçe", "English",
         "Source language: TR\nEnglish: Television"),
        ("Ağaç", "Türkçe", "Deutsch", "Source language: TR\nDeutsch: Baum"),
        ("Tree", "English", "Deutsch", "Source language: EN\nDeutsch: Baum"),
        ("Television", "English", "Türkçe",
         "Source language: EN\nTürkçe: Televizyon"),
    ])
    def test_valid_inputs(self, auth_key, in_text, src_lang, tgt_lang,
                          expected):
        """
        Test the "handle_translate" function with valid inputs.

        The expected ouptut is the translated word and the language of the
        base word.

        Args:
        - auth_key (str): the key for the Deepl API
        - in_text (str): the word to check and correct
        - src_lang (str): the language of the expression
        - tgt_lang (str): the target language for the translation
        - expected (str): the expected output for the given input

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        translation_field = tk.Label()
        handle_translate(key=auth_key, in_text=in_text, src_lang=src_lang,
                         tgt_lang=tgt_lang, enter_field=tk.Entry(),
                         translation_field=translation_field)
        assert translation_field.cget("text") == expected

    @pytest.mark.parametrize("in_text, src_lang, tgt_lang, entry_filed", [
        ("Baum", "Deutsch", "abc", tk.Entry()),
        ("Fernseher", "Deutsch", "TR", "abc"),
    ])
    def test_invalid_inputs(self, auth_key, in_text, src_lang, tgt_lang,
                            entry_filed):
        """
        Test the "handle_translate" function with invalid inputs.

        The expected ouptut is an empty string.

        Args:
        - auth_key (str): the key for the Deepl API
        - in_text (str): the word to check and correct
        - src_lang (str): the language of the expression
        - tgt_lang (str): the target language for the translation
        - entry_filed (tk.Entry): the entry field for the button

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        translation_field = tk.Label()
        with patch("tkinter.messagebox.showerror", return_value=True):
            handle_translate(key=auth_key, in_text=in_text, src_lang=src_lang,
                             tgt_lang=tgt_lang, enter_field=entry_filed,
                             translation_field=translation_field)
            assert translation_field.cget("text") == ""

    def test_empty_text(self, auth_key):
        """
        Test the "handle_translate" function with an empty text.

        The expected ouptut is an message that there is no text.

        Args:
        - auth_key (str): the key for the Deepl API

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        translation_field = tk.Label()
        with patch("tkinter.messagebox.showerror", return_value=True):
            handle_translate(key=auth_key, in_text="", src_lang="English",
                             tgt_lang="Deutsch", enter_field=tk.Entry(),
                             translation_field=translation_field)
            assert translation_field.cget("text") == ("No word entered. Please"
                                                      + " try again.")

    @pytest.mark.parametrize(("in_text, src_lang, tgt_lang, expected_trans,"
                              + "expected_entry"), [
        ("thiz is a test", "English", "Türkçe",
         "Source language: EN\nTürkçe: Bu bir test.", "this is a test"),
        ("das ist ein shcönes Haus", "Deutsch", "English",
         "Source language: DE\nEnglish: this is a beautiful house",
         "das ist ein schönes Haus"),
    ])
    def test_wrong_text(self, auth_key, in_text, src_lang, tgt_lang,
                        expected_trans, expected_entry):
        """
        Test the "handle_translate" function with incorrect written text.

        The expected ouptut is a translation and a corrected entry field if
        "yes" is selected in the messagebox, a translation and a not corrected
        entry filed it "no is selected and an empty strings if the "cancel"
        is selected

        Args:
        - auth_key (str): the key for the Deepl API
        - in_text (str): the word to check and correct
        - src_lang (str): the language of the expression
        - tgt_lang (str): the target language for the translation
        - expected_trans (str): the expected output of the translation field
        for the given input
        - expected_ent (str): the expected output of the entry field for the
        given input

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.askyesnocancel", return_value=True):
            translation_field = tk.Label()
            enter_field = tk.Entry()
            handle_translate(key=auth_key, in_text=in_text, src_lang=src_lang,
                             tgt_lang=tgt_lang, enter_field=enter_field,
                             translation_field=translation_field)
            assert translation_field.cget("text") == expected_trans
            assert enter_field.get() == expected_entry
        with patch("tkinter.messagebox.askyesnocancel", return_value=False):
            translation_field = tk.Label()
            enter_field = tk.Entry()
            handle_translate(key=auth_key, in_text=in_text, src_lang=src_lang,
                             tgt_lang=tgt_lang, enter_field=enter_field,
                             translation_field=translation_field)
            assert translation_field.cget("text") == expected_trans
            assert enter_field.get() == in_text
        with patch("tkinter.messagebox.askyesnocancel", return_value=None):
            translation_field = tk.Label()
            enter_field = tk.Entry()
            handle_translate(key=auth_key, in_text=in_text, src_lang=src_lang,
                             tgt_lang=tgt_lang, enter_field=enter_field,
                             translation_field=translation_field)
            assert translation_field.cget("text") == ""
            assert enter_field.get() == ""


class TestVocabularyInterface:
    """
    Test case for the "vocabulary_interface" function.

    This class defines test methods to ensure the "vocabulary_interface"
    function in the "interface_and_features" executes without error

    Attributes:
        - None

    Methods:
        - test_interface: Test the "vocabulary_interface" function without
        errors.
    """

    def test_interface(self):
        """
        Test the "vocabulary_interface" function without errors.

        The expected output is there is no Error during the execution.

        Args:
        - None

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch('tkinter.Tk') as mock_tk:
            vocabulary_interface()
            mock_tk.assert_called_once()
