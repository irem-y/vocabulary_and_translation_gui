import pytest
from unittest.mock import patch
from vocabulary_and_translation_gui.translation_and_spelling import (
    convert_language_name,
    check_spelling,
    correct_spelling_mistakes,
    translate_string
)
from vocabulary_and_translation_gui.prepare_application import (
    get_deepl_key
)


@pytest.fixture(scope="session")
def auth_key(pytestconfig):
    """Get the path of the Deepl Key."""
    path = pytestconfig.getoption("keypath")
    return get_deepl_key(file_path=path)


class TestConvertLanguageName:
    """
    Test cases for the "convert_language_name" function.

    This class defines test methods to ensure the "convert_language_name"
    function in the "translation_and_spelling" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_valid_input: Test the "convert_language_name" function with
        valid inputs.
        - test_invalid_input: Test the "convert_language_name" function with
        invalid inputs.
        - test_invalid_input_types: Test the "convert_language_name" function
        with invalid input types.
    """
    @pytest.mark.parametrize("abbr, style, expected", [
        ("Deutsch", "dic", "de_DE"),
        ("English", "tgt", "EN-GB"),
        ("Türkçe", "src", "TR"),
    ])
    def test_valid_input(self, abbr, style, expected, auth_key):
        """
        Test the "convert_language_name" function with valid inputs.

        The expected output is the correct abbrevation.

        Args:
        - abbr (str): the language abbreviation to convert
        - style (str): the style of the abbreviation (dic, src, tgt)
        - expected (str): the expected output for the given input

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        assert convert_language_name(abbr=abbr, style=style) == expected

    @pytest.mark.parametrize("abbr, style", [
        ("abc", "dic"),
        ("English", "abc"),
        ("", "src"),
        ("Deutsch", ""),
        ("", ""),
    ])
    def test_invalid_input(self, abbr, style):
        """
        Test the "convert_language_name" function with invalid inputs.

        The expected output is an empty string.

        Args:
        - abbr (str): the language abbreviation to convert
        - style (str): the style of the abbreviation (dic, src, tgt)

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        assert convert_language_name(abbr=abbr, style=style) == ""

    @pytest.mark.parametrize("abbr, style", [
        (["Deutsch", "English"], "dic"),
        ("Deutsch", ["dic", "tgt"]),
    ])
    def test_invalid_input_types(self, abbr, style):
        """
        Test the "convert_language_name" function with invalid input types.

        The expected output is a raised TypeError

        Args:
        - abbr (str): the language abbreviation to convert
        - style (str): the style of the abbreviation (dic, src, tgt)

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.showerror", return_value=True):
            with pytest.raises(TypeError,
                               match=("The input parameters have to be"
                                      + " strings!")):
                convert_language_name(abbr=abbr, style=style)


class TestCorrectSpellingMistakes:
    """
    Test cases for the "correct_spelling_mistakes" function.

    This class defines test methods to ensure the "correct_spelling_mistakes"
    function in the "translation_and_spelling" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_correct_words: Test the "correct_spelling_mistakes" function
        with correct written words.
        - test_incorrect_words: Test the "correct_spelling_mistakes" function
        with incorrect written words.
        - test_unknown_language: Test the "correct_spelling_mistakes" function
        with unknown source language.
        - test_unknown_words: Test the correct_spelling_mistakes function with
        too many or unknown inputs.
    """
    @pytest.mark.parametrize("in_text, dic_lang", [
        ("house", "English"),
        ("Haus", "Deutsch"),
        ("ev", "Türkçe"),
    ])
    def test_correct_words(self, in_text, dic_lang):
        """
        Test the "correct_spelling_mistakes" function without mistakes.

        The expected ouptut is the input word.

        Args:
        - in_text (str): the word to check and correct
        - dic_lang (str): the language of the word

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        assert correct_spelling_mistakes(in_text=in_text,
                                         dic_lang=dic_lang) == in_text

    @pytest.mark.parametrize("in_text, dic_lang, expected", [
        ("houze", "English", "house"),
        ("Hauss", "Deutsch", "Haus"),
        ("evv", "Türkçe", "ev"),
    ])
    def test_incorrect_words(self, in_text, dic_lang, expected):
        """
        Test the "correct_spelling_mistakes" function with mistakes.

        The expected output is the correct spelled version of the word.

        Args:
        - in_text (str): the word to check and correct
        - dic_lang (str): the language of the word
        - expected (str): the expected output for the given input

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        assert correct_spelling_mistakes(in_text=in_text,
                                         dic_lang=dic_lang) == expected

    @pytest.mark.parametrize("in_text, dic_lang, expected", [
        ("houze", "abc", "houze"),
        ("Hauss", "xyz", "Hauss"),
        ("evv", "", "evv"),
    ])
    def test_unknown_language(self, in_text, dic_lang, expected):
        """
        Test the "correct_spelling_mistakes" function with unknown language.

        The expected output is the input word.

        Args:
        - in_text (str): the word to check and correct
        - dic_lang (str): the language of the word
        - expected (str): the expected output for the given input

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        assert correct_spelling_mistakes(in_text=in_text,
                                         dic_lang=dic_lang) == expected

    @pytest.mark.parametrize("in_text, dic_lang", [
        ("askjsjjksajk", "English"),
        ("gfcvhjhsdkjs", "Deutsch"),
        ("Merhaba, nasılsın dostum?", "Türkçe"),
        ("Wie geht es dir?", "Deutsch"),
    ])
    def test_unknown_words(self, in_text, dic_lang):
        """
        Test the "correct_spelling_mistakes" function with wrong inputs.

        The expected outcome is the input word if "yes" is selected in the
        messagebox and an ValueError if "no" is selected.

        Args:
        - in_text (str): the word to check and correct
        - dic_lang (str): the language of the word

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.askyesno", return_value=True):
            assert correct_spelling_mistakes(in_text=in_text,
                                             dic_lang=dic_lang) == in_text

        with patch("tkinter.messagebox.askyesno", return_value=False):
            with pytest.raises(ValueError, match="Expression not found"):
                correct_spelling_mistakes(in_text=in_text, dic_lang=dic_lang)


class TestCheckSpelling:
    """
    Test cases for the "check_spelling" function.

    This class defines test methods to ensure the "check_spelling"
    function in the "translation_and_spelling" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_correct_expression:Test the "check_spelling" function with
        correct written expressions.
        - test_incorrect_expression: Test the "check_spelling" function with
        incorrect written expressions.
        - test_unknown_expression: Test the "check_spelling function with
        unknown inputs.
        - test_unknown_language: Test the "check_spelling" function with
        a unknown language.
    """
    @pytest.mark.parametrize("in_text, lang", [
        ("the house is small", "English"),
        ("das Haus ist klein", "Deutsch"),
        ("küçük ev", "Türkçe"),
    ])
    def test_correct_expression(self, in_text, lang):
        """
        Test the "check_spelling" function with correct written expressions.

        The expected ouptut is the input word.

        Args:
        - in_text (str): the word to check and correct
        - lang (str): the language of the word

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        assert check_spelling(in_text=in_text, lang=lang) == in_text

    @pytest.mark.parametrize("in_text, lang, expected", [
        ("the houze is smalll", "English", "the house is small"),
        ("der Baumm ist klain", "Deutsch", "der Baum ist klein"),
        ("Armuti çok lezetli", "Türkçe", "Armut çok lezzetli"),
    ])
    def test_incorrect_expression(self, in_text, lang, expected):
        """
        Test the "check_spelling" function with incorrect written expressions.

        The expected output is the corrected expression if "yes" is selected
        in the messagebox, the input expression if "no" is selscted, and a
        ValueError if the "cancel is selected.

        Args:
        - in_text (str): the word to check and correct
        - lang (str): the language of the word
        - expected (str): the expected output for the given input

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.askyesnocancel", return_value=True):
            assert check_spelling(in_text=in_text, lang=lang) == expected

        with patch("tkinter.messagebox.askyesnocancel", return_value=False):
            assert check_spelling(in_text=in_text, lang=lang) == in_text

        with patch("tkinter.messagebox.askyesnocancel", return_value=None):
            with pytest.raises(ValueError, match="Expression not found"):
                check_spelling(in_text="Armuti çok lezetli", lang="Türkçe")

    @pytest.mark.parametrize("in_text, lang", [
        ("askjsjjksajk", "English"),
        ("gfcvhjhsdkjs", "Deutsch"),
    ])
    def test_unknown_expression(self, in_text, lang):
        """
        Test the "check_spelling" function with unknown inputs.

        The expected outcome is the input word if "yes" is selected in the
        messagebox and an ValueError if "no" is selected.

        Args:
        - in_text (str): the word to check and correct
        - lang (str): the language of the word

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.askyesno", return_value=True):
            assert check_spelling(in_text=in_text, lang=lang) == in_text

        with patch("tkinter.messagebox.askyesno", return_value=False):
            with pytest.raises(ValueError, match="Expression not found"):
                check_spelling(in_text=in_text, lang=lang)

    @pytest.mark.parametrize("in_text, lang", [
        ("the house is small", "abc"),
        ("das Hauss ist klain", "xyz"),
        ("küçük ev", "Türkçe"),
    ])
    def test_unknown_language(self, in_text, lang):
        """
        Test the "check_spelling" function with a unknown language.

        The expected ouptut is the input word.

        Args:
        - in_text (str): the word to check and correct
        - lang (str): the language of the word

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        assert check_spelling(in_text=in_text, lang=lang) == in_text


class TestTranslateString:
    """
    Test cases for the "translate_string" function.

    This class defines test methods to ensure the "translate_string"
    function in the "translation_and_spelling" module handles valid and invalid
    inputs correctly.

    Attributes:
        - None

    Methods:
        - test_valid_inputs: Test the "test_valid_inputs" function with valid
        inputs.
        - test_invalid_inputs: Test the "test_invalid_inputs" function with
        invalid inputs.
        - test_invalid_key: Test the "test_invalid_inputs" function with wrong
        Deepl Key.
    """
    @pytest.mark.parametrize("in_text, src_lang, tgt_lang, expected", [
        ("Baum", "Deutsch", "English", ("Tree", "DE")),
        ("Fernseher", "Deutsch", "Türkçe", ("Televizyon", "DE")),
        ("Televizyon", "Türkçe", "English", ("Television", "TR")),
        ("Ağaç", "Türkçe", "Deutsch", ("Baum", "TR")),
        ("Tree", "English", "Deutsch", ("Baum", "EN")),
        ("Television", "English", "Türkçe", ("Televizyon", "EN")),
    ])
    def test_valid_inputs(self, auth_key, in_text, src_lang, tgt_lang,
                          expected):
        """
        Test the "test_valid_inputs" function with valid inputs.

        The test runs with the source language provided and not provided.
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
        assert translate_string(auth_key=auth_key, in_text=in_text,
                                src_lang=src_lang,
                                tgt_lang=tgt_lang) == expected
        assert translate_string(auth_key=auth_key, in_text=in_text,
                                src_lang="", tgt_lang=tgt_lang) == expected

    @pytest.mark.parametrize("in_text, src_lang, tgt_lang, error_msg", [
        ("", "Deutsch", "English", "No text to tranlsate were found."),
        ("Tree", "English", "abc", "Target Language is unknown."),
    ])
    def test_invalid_inputs(self, auth_key, in_text, src_lang, tgt_lang,
                            error_msg):
        """
        Test the "test_invalid_inputs" function with invalid inputs.

        The expected ouptut is a raised ValueError with a message based on the
        missing or wrong parameter.

        Args:
        - auth_key (str): the key for the Deepl API
        - in_text (str): the word to check and correct
        - src_lang (str): the language of the expression
        - tgt_lang (str): the target language for the translation
        - error_msg (str): the expected raised error message

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.showerror", return_value=True):
            with pytest.raises(ValueError, match=error_msg):
                translate_string(auth_key=auth_key, in_text=in_text,
                                 src_lang=src_lang, tgt_lang=tgt_lang)

    def test_invalid_key(self):
        """
        Test the "test_invalid_inputs" function with wrong Deepl Key.

        The expected ouptut is a raised ValueError.

        Args:
        - None

        Raises:
        - AssertionError: if the output of the function does not match the
        expected value
        """
        with patch("tkinter.messagebox.showerror", return_value=True):
            with pytest.raises(ValueError,
                               match=("The provided Deepl authentication key"
                                      + " is invalid or unauthorized.")):
                translate_string(auth_key="abc", in_text="Tree", src_lang="EN",
                                 tgt_lang="DE")
