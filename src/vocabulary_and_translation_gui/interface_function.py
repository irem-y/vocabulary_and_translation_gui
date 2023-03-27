"""
Functions for creating an user interface.

Functions:
- vocabulary_interface(deepl_key)
"""

from save_functions import save_button
import tkinter as tk
from translation_functions import (
    translate_button,
    add_word_button
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
                             command=lambda: translate_button(
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
                           command=lambda: add_word_button(
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
                                 command=lambda: save_button(new_vocabularies))
    save_file_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Add a button to quit the program
    end_button = tk.Button(user_interface, text='Quit',
                           command=user_interface.destroy)
    end_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Run the tkinter main loop
    user_interface.mainloop()
