"""
All functions for saving a word list.

Functions:
- save_list_as_apkg(word_list, path)
- save_list_as_xlsx(word_list, path)
"""

import genanki
import os
import pandas as pd
import random
from tkinter import messagebox


def save_list_as_apkg(word_list=[], path=""):
    """
    Save the given word list as an Anki (.apkg) file at the given path.

    Args:
    - word_list (list): A list of tuples containing English, German, and
    Turkish words.
    - path (str): The path to save the Anki (.apkg) file.

    Returns:
        None
    """
    # Messages and titles for the message boxes shown to the user
    messages = {
        "empty": "No words to save were found.",
        "four": ("There have to be exactly four entries in each entry of"
                 + " word_list."),
        "error": ("Error: This program doesn't have access to this path: "
                  + path),
        "success": (str(len(word_list)) + " new word(s) added to the "
                    "vocabulary list Anki file.")
    }

    titles = {
        "empty": "No words found",
        "four": "Not four entries",
        "error": "ERROR",
        "success": "Save successful"
    }

    # Check if the word_list is empty
    if len(word_list) <= 0:
        messagebox.showwarning(title=titles["empty"],
                               message=messages["empty"])
        return

    # Check if word_list has exactly 4 entries
    for short_list in word_list:
        if len(short_list) != 4:
            messagebox.showwarning(title=titles["four"],
                                   message=messages["four"])
            return
    # If the directory for the file not exist, a new directory get created
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    # Create a new Anki model with unique model_id
    model_id = random.randrange(1 << 30, 1 << 31)
    vocabulary_model = genanki.Model(
        model_id,
        'New Words',
        fields=[
            {'name': 'Question'},
            {'name': 'AnswerEn'},
            {'name': 'AnswerTr'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">'
                        + '{{AnswerEn}}<br>{{AnswerTr}}',
            },
        ]
    )

    # Create a new Anki deck with unique deck_id
    deck_id = random.randrange(1 << 30, 1 << 31)
    vocabulary_deck = genanki.Deck(deck_id, "German Vocabulary")

    # Add each word from the word list as a new note to the deck
    for entry in word_list:
        new_note = genanki.Note(
            model=vocabulary_model,
            fields=[
                "Deutsch: " + entry[1],
                "English: " + entry[0],
                "Türkçe: " + entry[2]
            ]
        )
        vocabulary_deck.add_note(new_note)

    # Write the deck to the Anki (.apkg) file at the given path
    try:
        genanki.Package(vocabulary_deck).write_to_file(path)
    except PermissionError:
        # Show an error message to the user if there access gets denied
        messagebox.showerror(title=titles["error"], message=messages["error"])
        return

    # Show a success message with the number of words added vocabularies
    messagebox.showinfo(title=titles["success"], message=messages["success"])


def save_list_as_xlsx(word_list=[], path=""):
    """
    Save a list of words in an Excel file located in the specified path.

    The Excel file will contain a sheet named 'Vocabulary' and will have
    columns for English, Deutsch, Türkçe, and Timestamp.

    Args:
    - word_list (list of tuples): List of tuples containing the words to be
    saved.
    - path (str): Path to the Excel file to be created or updated.

    Returns:
    - None
    """
    # Messages and titles for the message boxes shown to the user
    messages = {
        "empty": "No words to save were found.",
        "four": ("There have to be exactly four entries in each entry of "
                 + "word_list."),
        "error": ("Error: The Excel file in the path:" + path + "is either"
                  "being opened by another application and must be closed,"
                  "or this program doesn't have access to this file."),
        "success": (str(len(word_list)) + " new word(s) added to the "
                    "vocabulary list Excel file.")
    }

    titles = {
        "empty": "No words found",
        "four": "Not four entries",
        "error": "ERROR",
        "success": "Save successful"
    }
    # Check if the word_list is empty
    if len(word_list) <= 0:
        messagebox.showwarning(title=titles["empty"],
                               message=messages["empty"])
        return

    # Check if word_list has exactly 4 entries
    for short_list in word_list:
        if len(short_list) != 4:
            messagebox.showwarning(title=titles["four"],
                                   message=messages["four"])
            return

    # If the directory for the file not exist, a new directory get created
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    # Create a pandas data frame with the word_list data
    df = pd.DataFrame(word_list,
                      columns=['English', 'Deutsch', 'Türkçe', 'Timestamp'])

    # Set the 'Timestamp' column as the index of the data frame
    df.set_index('Timestamp', inplace=True, drop=True)

    # Check if the Excel file already exists in the specified path
    if os.path.exists(path):
        while True:
            try:
                # Open the Excel file in append mode and write the data frame
                with pd.ExcelWriter(path,
                                    mode='a',
                                    engine="openpyxl",
                                    if_sheet_exists="overlay") as writer:
                    df.to_excel(writer, sheet_name='Vocabulary',
                                startrow=writer.sheets['Vocabulary'].max_row,
                                header=False)
            except PermissionError:
                # Show an error message to the user if the file is being used
                # by another program
                if messagebox.askretrycancel(
                    title=titles["error"],
                    message=messages["error"]
                                            ) is False:
                    break
            else:
                # Show a success message to the user if the file was
                # successfully written
                messagebox.showinfo(title=titles["success"],
                                    message=messages["success"])
                break
    else:
        # If the Excel file does not exist, create it and write the data frame
        df.to_excel(path, sheet_name='Vocabulary')
        messagebox.showinfo(title=titles["success"],
                            message=messages["success"])
