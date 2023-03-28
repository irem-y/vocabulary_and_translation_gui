"""
Function for creating an user interface and the functions for the buttons.

Functions:
- vocabulary_interface(deepl_key)
- handle_translate(key, in_text, src_lang, tgt_lang, enter_field,
                   translation_field)
- handle_add_to_list(key, in_text, src_lang, enter_field, translation_field,
                  trans_list_field, trans_list)
- handle_save(vocabulary_list)
"""

import datetime
import tkinter as tk
import os
from tkinter import (
    filedialog,
    messagebox
)
from vocabulary_and_translation_gui.save_list import (
    save_list_as_apkg,
    save_list_as_xlsx
)
from vocabulary_and_translation_gui.translation_and_spelling import (
    translate_string,
    check_spelling
)


def vocabulary_interface(deepl_key=""):
    """
    Create a GUI for a vocabulary list application with translation.

    Allows users to enter text and translate it between different languages,
    add the translated text to a vocabulary list, and save the vocabulary
    list to a file.

    Args:
    - deepl_key (str): Key for the translation functions with deepl

    Returns:
    - None
    """
    # Create an empty list to store new vocabularies
    new_vocabularies = []

    # Create a tkinter instance
    user_interface = tk.Tk()
    user_interface.title('Translater & Vocabulary interface')

    # Add a label for the user input field
    tk.Label(user_interface, text="Your Expression:").pack()

    # Add an entry field for user input
    entry_field = tk.Entry(user_interface, width=50)
    entry_field.pack()

    # Add a label for the translation field
    translation_field = tk.Label(user_interface)
    translation_field.pack()

    # Add a label for the vocabulary list
    vocabularies_overview = tk.Label(user_interface)
    vocabularies_overview.pack()

    # Create a dropdown menu for the source language selection
    source_languages = [
        "English",
        "Deutsch",
        "Türkçe",
        "Automatic language recognition"
    ]
    tk.Label(user_interface, text="Source Language:").pack()
    src_lang_sel = tk.StringVar(user_interface)
    src_lang_sel.set(source_languages[1])
    dropdown_source_language = tk.OptionMenu(user_interface,
                                             src_lang_sel,
                                             *source_languages)
    dropdown_source_language.pack()

    # Create a dropdown menu for the target language selection
    target_languages = [
        "English",
        "Deutsch",
        "Türkçe"
    ]
    tk.Label(user_interface, text="Target Language:").pack()
    tgt_lang_sel = tk.StringVar(user_interface)
    tgt_lang_sel.set(target_languages[0])
    dropdown_target_language = tk.OptionMenu(user_interface,
                                             tgt_lang_sel,
                                             *target_languages)
    dropdown_target_language.pack()

    # Add a button to translate user input
    trans_button = tk.Button(user_interface, text='Translate',
                             command=lambda: handle_translate(
                                                deepl_key,
                                                entry_field.get(),
                                                src_lang_sel.get(),
                                                tgt_lang_sel.get(),
                                                entry_field,
                                                translation_field
                                                )
                             )
    trans_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Add a button to add user input to vocabulary list
    add_button = tk.Button(user_interface, text='Add to vocabulary list',
                           command=lambda: handle_add_to_list(
                                                deepl_key,
                                                entry_field.get(),
                                                src_lang_sel.get(),
                                                entry_field,
                                                translation_field,
                                                vocabularies_overview,
                                                new_vocabularies
                                                )
                           )
    add_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Add a button to save vocabulary list to a file
    save_file_button = tk.Button(user_interface, text='Save vocabulary list',
                                 command=lambda: handle_save(new_vocabularies))
    save_file_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Add a button to quit the program
    end_button = tk.Button(user_interface, text='Quit',
                           command=user_interface.destroy)
    end_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Run the tkinter main loop
    user_interface.mainloop()


def handle_translate(key="", in_text="", src_lang="", tgt_lang="",
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

        # Translate input text
        try:
            output = translate_string(key, correct_text,
                                      src_lang, tgt_lang)
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


def handle_add_to_list(key="", in_text="", src_lang="", enter_field=None,
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
        language_list = ["English", "Deutsch", "Türkçe"]

        # Get current upload list and add new word to it
        translation_list_str = str(trans_list_field.cget("text"))
        if len(translation_list_str) <= 0:
            translation_list_str = "Upload list:\n"
        else:
            translation_list_str += "\n"

        # Translate the entered word to each language in the language_list
        # and add the translations to the upload list string
        tmp_word_list = []
        for lang in language_list:
            try:
                output = translate_string(key, correct_text, src_lang, lang)
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


def handle_save(vocabulary_list=[]):
    """
    Save the vocabulary list as an Anki or Excel file.

    Args:
    - vocabulary_list (list): List of tuples containing English, German,
    and Turkish words.

    Returns:
    - None
    """
    # Define titles and messages for the message boxes
    messages = {
        "info": ("If an existing file is selected, a window will appear "
                 "asking if the file should be replaced. If 'yes' is "
                 "selected, Anki (.apkg) files will be replaced and Excel "
                 "(.xlsx) files will be appended."),
        "filetype": "Please choose .xlsx or .apkg as file type.",
        "path": "No path selected.",
        "empty": "No words to add were found."
    }

    titles = {
        "info": "Information",
        "filetype": "Save the file as an Anki or Excel file",
        "path": "Warning",
        "empty": "Save not successful"
    }

    # Check if there are words in the vocabulary list
    if not vocabulary_list:
        messagebox.showwarning(title=titles["empty"],
                               message=messages["empty"])
        return

    # Display the "replace" information message
    messagebox.showinfo(title=titles["info"], message=messages["info"])

    while True:
        # Open a dialog box to get a file name and path
        file_path = filedialog.asksaveasfilename(
            title=titles["filetype"],
            initialdir="./",
            filetypes=[
                ("Anki file (.apkg)", "*.apkg"),
                ("Excel file (.xlsx)", "*.xlsx"),
                ("All files", "*.*")
            ],
            defaultextension=".apkg",
            initialfile="vocabulary_list"
        )

        # Check if a file path was provided
        if not file_path:
            # If no path was selected, ask the user to retry or cancel
            if not messagebox.askretrycancel(title=titles["path"],
                                             message=messages["path"]):
                break
            continue

        # Get the extension of the selected file
        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".apkg":
            # Call a function to save the vocabulary list as an Anki file
            save_list_as_apkg(vocabulary_list, file_path)
            break
        elif extension == ".xlsx":
            # Call a function to save the vocabulary list as an Excel file
            save_list_as_xlsx(vocabulary_list, file_path)
            break
        else:
            # If the extension is unsupported, ask the user to retry or cancel
            if not messagebox.askretrycancel(title=titles["filetype"],
                                             message=messages["filetype"]):
                break
            continue
