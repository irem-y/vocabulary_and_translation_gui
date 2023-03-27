"""
All functions for translating and correcting expressions.

Functions:
- translate_string(auth_key, in_text, src_lang, tgt_lang)
- convert_abbreviation(abbr, style)
- translate_button(key, in_text, src_lang, tgt_lang, enter_field,
                   translation_field)
- add_word_button(key, in_text, src_lang, enter_field, translation_field,
                  trans_list_field, trans_list)
- check_spelling(in_text, lang)
- replace_wrong_words(in_text, dic_lang)
"""

import datetime
import deepl
import enchant
import re
from tkinter import messagebox
import tkinter as tk


def translate_button(key="", in_text="", src_lang="", tgt_lang="",
                     enter_field=None, translation_field=None):
    """
    Translate the input text and displays the result in the translation_field.

    The input text get translated with translate_string from the source
    language to the target language and displays the translation and source
    language in the translation_field.

    Args:
    - in_text (str): The input text to be translated.
    - src_lang (str): The source language of the input text.
    - tgt_lang (str): The target language for the translation.
    - enter_field (tk.Entry): The input field for entering the text.
    - translation_field (tk.Label): The field for displaying the translation
    and source language.

    Returns:
    - None
    """
    # Create titles and messages for error messages
    titles = {
        "key": "key must be a string",
        "in_text": "in_text must be a string",
        "src_lang": "src_lang must be a string",
        "tgt_lang": "tgt_lang must be a string",
        "enter_field": "enter_field must be a tkinter Entry widget",
        "translation_field": ("translation_field must be a tkinter Label "
                              + "widget")
    }
    messages = {
        "key": "The input variable key must be a string",
        "in_text": "The input variable in_text must be a string",
        "src_lang": "The input variable src_lang must be a string",
        "tgt_lang": "The input variable tgt_lang must be a string",
        "enter_field": ("The input variable enter_field must be a tkinter "
                        + "Entry widget"),
        "translation_field": ("The input variable translation_field must be a"
                              + " tkinter Label widget")
    }
    # Check types of function parameters
    if not isinstance(key, str):
        messagebox.showerror(title=titles["key"], message=messages["key"])
        return
    if not isinstance(in_text, str):
        messagebox.showerror(title=titles["in_text"],
                             message=messages["in_text"])
        return
    if not isinstance(src_lang, str):
        messagebox.showerror(title=titles["src_lang"],
                             message=messages["src_lang"])
        return
    if not isinstance(tgt_lang, str):
        messagebox.showerror(title=titles["tgt_lang"],
                             message=messages["tgt_lang"])
        return
    if not isinstance(enter_field, tk.Entry):
        messagebox.showerror(title=titles["enter_field"],
                             message=messages["enter_field"])
        return
    if not isinstance(translation_field, tk.Label):
        messagebox.showerror(title=titles["translation_field"],
                             message=messages["translation_field"])
        return

    # If input text is not empty
    if len(in_text) > 0:

        # Check spelling of input text
        try:
            correct_text = check_spelling(in_text, src_lang)
        except ValueError:
            # If input text contains unrecognized words empty the
            # display filed and do nothing more
            translation_field.configure(text="")
            return

        # Clear input field and insert corrected text
        enter_field.delete(0, tk.END)
        enter_field.insert(0, correct_text)

        # Convert language abbreviations to required format
        try:
            input_lang = convert_abbreviation(src_lang, "src")
        except TypeError:
            return
        try:
            output_lang = convert_abbreviation(tgt_lang, "tgt")
        except TypeError:
            return

        # Translate input text
        try:
            output = translate_string(key, correct_text,
                                      input_lang, output_lang)
        except ValueError:
            return

        # Format translation and source language for display
        msg = (
            "Source language: " + str(output[1]) + "\n" + tgt_lang
            + ": " + str(output[0])
        )

        # Display translation and source language
        translation_field.configure(text=msg)

    # If input text is empty display a info message
    else:
        translation_field.configure(text="No word entered. Please try again.")


def add_word_button(key="", in_text="", src_lang="", enter_field=None,
                    translation_field=None, trans_list_field=None,
                    trans_list=[]):
    """
    Add a word to the translation upload list.

    Args:
        - in_text (str): The word to be added to the upload list.
        - src_lang (str): The source language of the word.
        - enter_field (tk.Entry): The Tkinter Entry widget where the user
        inputs the word.
        - translation_field (tk.Label): The Tkinter Label widget where feedback
        messages are displayed.
        - trans_list_field (tk.Label): The Tkinter Label widget where the
        current upload list is displayed.
        - trans_list (list): The list where uploaded words are stored.

    Returns:
        - list: The updated list of uploaded words.
    """
    # Create titles and messages for error messages
    titles = {
        "key": "key must be a string",
        "in_text": "in_text must be a string",
        "src_lang": "src_lang must be a string",
        "enter_field": "enter_field must be a tkinter Entry widget",
        "translation_field": ("translation_field must be a tkinter Label "
                              + "widget"),
        "trans_list": "trans_list must be a list"
    }
    messages = {
        "key": "The input variable key must be a string",
        "in_text": "The input variable in_text must be a string",
        "src_lang": "The input variable src_lang must be a string",
        "enter_field": ("The input variable enter_field must be a tkinter "
                        + "Entry widget"),
        "translation_field": ("The input variable translation_field must be a"
                              + " tkinter Label widget"),
        "trans_list": "The input variable trans_list must be a list"
    }
    # Check types of function parameters
    if not isinstance(key, str):
        messagebox.showerror(title=titles["key"], message=messages["key"])
        return
    if not isinstance(in_text, str):
        messagebox.showerror(title=titles["in_text"],
                             message=messages["in_text"])
        return
    if not isinstance(src_lang, str):
        messagebox.showerror(title=titles["src_lang"],
                             message=messages["src_lang"])
        return
    if not isinstance(enter_field, tk.Entry):
        messagebox.showerror(title=titles["enter_field"],
                             message=messages["enter_field"])
        return
    if not isinstance(translation_field, tk.Label):
        messagebox.showerror(title=titles["translation_field"],
                             message=messages["translation_field"])
        return
    if not isinstance(trans_list, list):
        messagebox.showerror(title=titles["trans_list"],
                             message=messages["trans_list"])
        return

    # Check if word is entered
    if len(in_text) > 0:
        try:
            # Check spelling of the entered word
            correct_text = check_spelling(in_text, src_lang)
        except ValueError:
            # If input text contains unrecognized words do nothing
            return

        # List of abbreviated languages for translation
        abbr_list = ["EN-GB", "DE", "TR"]

        # Convert source language to its abbreviation
        try:
            input_lang = convert_abbreviation(src_lang, "src")
        except TypeError:
            return

        # Get current upload list and add new word to it
        translation_list_str = str(trans_list_field.cget("text"))
        if len(translation_list_str) <= 0:
            translation_list_str = "Upload list:\n"
        else:
            translation_list_str += "\n"

        # Translate the entered word to each language in the abbr_list
        # and add the translations to the upload list string
        tmp_word_list = []
        for lang in abbr_list:
            try:
                output = translate_string(key, correct_text, input_lang, lang)
            except ValueError:
                return
            tmp_word_list.append(output[0])
            translation_list_str += f"{lang}: {output[0]}, "
        translation_list_str = translation_list_str[:-2]
        trans_list_field.configure(text=translation_list_str)

        # Add the translated words and the current datetime to trans_list
        tmp_word_list.append(str(datetime.datetime.now()))
        trans_list.append(tmp_word_list)

        # Clear the input field
        enter_field.delete(0, tk.END)

        # Display feedback message indicating that the entered word was added
        # to the upload list along with the source language
        translation_field.configure(text=f"Translation: '{correct_text}'"
                                    f"added to upload list. Source language: "
                                    f"{output[1]}")

        return trans_list
    else:
        # Display feedback message if no word was entered
        translation_field.configure(text="No word entered. Please try again.")


def translate_string(auth_key="", in_text="", src_lang="", tgt_lang=""):
    """Translate a string from a source language to target language.

    Args:
    - in_text (str): String to be translated.
    - src_lang (str): Source language code. If None, the language is
    automatically detected by the API.
    - tgt_lang (str): Target language code for translation.

    Returns:
    - Tuple of two strings: The translated text and detected source
    language of the input string.

    Raises:
    - ValueError: If the provided authentication key is invalid or
    unauthorized.
    - ValueError: If no text is entered for translation.
    - ValueError: If the target language is unknown or not supported by the
    API.
    """
    # Creating Titles and messages for the errors
    titles = {
        "auth": "Wrong authentification Key",
        "text": "Text needed",
        "lang": "Unknown target language"
    }
    messages = {
        "auth": ("The provided Deepl authentication key is invalid or "
                 + "unauthorized."),
        "text": "No text to tranlsate were found.",
        "lang": "Target Language is unknown."
    }
    # Initialize the translator object with the authentication key
    translator = deepl.Translator(auth_key)

    # Call the `translate_text` method of the translator object to translate
    # the input string with the specified source and target languages
    try:
        result = translator.translate_text(
            in_text, source_lang=src_lang,
            target_lang=tgt_lang
        )
    except deepl.exceptions.AuthorizationException:
        # If the provided authentication key is invalid or unauthorized,
        # display an error message and raise a ValueError with the message.
        messagebox.showerror(title=titles["auth"], message=messages["auth"])
        raise ValueError(messages["auth"])
    except ValueError:
        # If no text is entered for translation, display an error message
        # and raise a ValueError with the message.
        messagebox.showerror(title=titles["text"], message=messages["text"])
        raise ValueError(messages["text"])
    except deepl.exceptions.DeepLException:
        # If the target language is not supported by the API or unknown,
        # display an error message and raise a ValueError with the message.
        messagebox.showerror(title=titles["lang"], message=messages["lang"])
        raise ValueError(messages["lang"])

    # Return the translated text and detected source language as a tuple
    return result.text, result.detected_source_lang


def convert_abbreviation(abbr="", style=""):
    """Convert a language name abbreviation to a specific format.

    The `abbr` parameter should be a string containing the full name of the
    language (e.g. "English", "Deutsch", "Türkçe"). The `style` parameter
    specifies the format to convert the abbreviation to. The following styles
    are supported:

    - "dic": Abbreviation for use in an enchant dictionary, e.g. "en_GB".
    - "src": Abbreviation for use as the source language in translation, e.g.
      "EN".
    - "tgt": Abbreviation for use as the target language in translation, e.g.
      "EN-GB".

    Args:
    - abbr (str): Full name of the language.
    - style (str): Style to convert the abbreviation to.

    Returns:
    - str: Abbreviation in the specified format, or an empty string if the
    input abbreviation is not recognized.

    Raises:
    - TypeError: If the input parameters are not strings.
    """
    # Define a dictionary that maps full language names to their
    # corresponding abbreviations
    abbr_dict = {
        "Deutsch": {"dic": "de_DE", "src": "DE", "tgt": "DE"},
        "English": {"dic": "en_GB", "src": "EN", "tgt": "EN-GB"},
        "Türkçe": {"dic": "tr_TR", "src": "TR", "tgt": "TR"}
    }

    try:
        # Return the abbreviation in the specified format
        return abbr_dict[abbr][style]
    except KeyError:
        # If abbr or style is not in abbr_dict, return an empty string
        return ""
    except TypeError:
        # If abbr or style has an unhashable type, show an error message
        msg = "The language name and abbrevation style has to be strings!"
        messagebox.showerror(title="Wrong parameter types", message=msg)
        raise TypeError("The input parameters have to be strings!")


def check_spelling(in_text="", lang=""):
    """
    Check the spelling of a given text in the specified language.

    Args:
    - in_text (str): Text to check the spelling of.
    - lang (str): Language to check the spelling in.
    If "Automatic language recognition" is given, a warning is returned.

    Returns:
    - str: The corrected text if errors were found, otherwise the original
    text.

    Raises:
    - ValueError: If the expression could not be found
    """
    # If the specified language is "Automatic language recognition", return the
    # input text without performing any spell-checking
    if lang not in ["English", "Deutsch", "Türkçe"]:
        return in_text

    # Split the input text into words and punctuation using a regular
    # expression
    split_text = re.findall(r"[\w']+|[.,!?;: ]", in_text)
    try:
        # For each word in the split text, replace any incorrect spelling with
        # a corrected version using the specified language
        correct_text_lst = [replace_wrong_words(word, lang)
                            for word in split_text]
    except ValueError:
        # If a value error is raised when calling replace_wrong_words, raise
        # a new ValueError with the message "Expression not found"
        raise ValueError("Expression not found")

    # Join the corrected words and punctuation back into a single string
    correct_text = "".join(correct_text_lst)

    # If the corrected text is different from the original text, prompt the
    # user to confirm if they want to use the corrected text or not
    if in_text != correct_text:
        msg = (
            "This expression is incorrect:\n" + in_text
            + "\n\nThe correct expression could be:\n" + correct_text
            + "\n\nDo you want to use the corrected expression?"
        )
        msg_title = "Incorrect expression found"
        choice = messagebox.askyesnocancel(title=msg_title,
                                           message=msg)
        if choice is None:
            # If the user selects "Cancel", raise a new ValueError with the
            # message "Expression not found"
            raise ValueError("Expression not found")
        elif choice is True:
            # If the user selects "Yes", return the corrected text
            return correct_text
        else:
            # If the user selects "No", return the original text
            return in_text
    else:
        # If the corrected text is the same as the original text, return the
        # original text
        return in_text


def replace_wrong_words(in_text="", dic_lang=""):
    """
    Replace misspelled words with the most likely correct spelling.

    Args:
    - in_text (str): Text to replace the misspelled words in.
    - dic_lang (str): Language to check the spelling against.

    Returns:
    - str: The corrected word if an error was found, otherwise the original
    word.

    Raises:
    - ValueError: If the expression is not found
    """
    # Message and titles
    titles = {
        "expression": "Expression not found"
    }

    messages = {
        "expression": (
                "Following expression either not exist or is in "
                + "the wrong language:\n" + in_text
                + "\n\nDo you want to continue with this expression?"
                )
    }
    # Create a dictionary checker for the specified language, if no dictionary
    # is found return the input sting
    try:
        dictionary_language = convert_abbreviation(dic_lang, "dic")
    except TypeError:
        return

    # Check if the needed dictionary exist
    try:
        txt_chkr = enchant.Dict(dictionary_language)
    except enchant.errors.DictNotFoundError:
        return in_text

    # Create a list of punctuation marks and spaces
    punctuation_list = [".", ",", "!", "?", ";", ":", " "]

    # Check if word is spelled correct
    try:
        word_is_correct = txt_chkr.check(in_text)
    except enchant.errors.Error:
        return in_text

    # If the word is a punctuation mark or is correctly spelled, return the
    # original word
    if in_text in punctuation_list or word_is_correct is True:
        return in_text
    else:
        # If the word is misspelled, suggest the most likely correct spelling
        correct = txt_chkr.suggest(in_text)

        # If there is at least one suggestion, return the first one
        if len(correct) > 0:
            return correct[0]
        else:
            # If there are no suggestions, prompt the user with a message box
            # to either continue or stop
            # If the user clicks 'Yes', return the original word, otherwise
            # raise an error
            if messagebox.askyesno(title=titles["expression"],
                                   message=messages["expression"]):
                return in_text
            else:
                raise ValueError(titles["expression"])
