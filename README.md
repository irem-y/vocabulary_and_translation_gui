# Vocabulary and Translation GUI

#### Effective Programming Practices for Economists

#### Winter Term 2022/23

#### Ayse Irem Yilmaz <br /><br />

## Description

This application provides a graphical user interface (GUI) with translation and vocabulary learning features. 

You can enter an English, German or Turkish words or phrases into the interface.
The application can then translate the word or phrase into your choice of English, German or Turkish. 
You can also add the phrase to a vocabulary list and then save the list as an Excel file or Anki file.

I developed and tested the code on Microsoft Windows 10.<br /><br />

## Preperation

### Clone the repository

First clone the repository into a local directory

```console
$ git clone https://github.com/irem-y/vocabulary_and_translation_gui
```

### Get a DeepL key

As a next step create an DeepL account for free to get your personal authentication key.

[Here](https://www.deepl.com/en/signup/?cta=free-login-signup/) can you create an account and [here](https://www.deepl.com/account/summary) can you see your key in you account under "Authentication Key for DeepL API".

In the project folder  `src/vocabulary_and_translation_gui/resources` you can find the text file `deepl_key.txt`.    
Please add [here](src/vocabulary_and_translation_gui/resources/deepl_key.txt) your personal key.

### Creating the conda environment
To get started, navigate to the project folder and create the environment with the `environment.yml` file:

```console
$ conda env create -f environment.yml
```

And activate the environment with:
```console
$ conda activate vocabulary_and_translation_gui
```

### Building the project
To build the project, type:

```console
$ pytask
```
The last task will create the GUI. You can already use it here, but if you run pytask after the initial run, the GUI will not be created. For the general usage of the GUI, see under the chapter [Interface Usage](#Interface-Usage)

If a message box appears during this process, follow the instructions in the message. 

During this process the text files `dicts_ckeck_result.txt`, `key_ckeck_result.txt` and `pytest_ckeck_result.txt` are created. 

Check these files [here](BLD) to see if there are any problems.

A message box may appear saying that not all of the required dictionaries are included in the enchant package. 
To add the dictionaries follow the instructions in the message box. The required dictionaries can be found [here](src/vocabulary_and_translation_gui/resources/dictionaries).

### Optional
To use the Anki files that can be created while using the interface, to learn vocabulary, download Anki for free [here](https://apps.ankiweb.net/). 

## Interface Usage
To open the GUI run the file `create_interface.py`. It can be found [here](src/vocabulary_and_translation_gui/create_interface.py).

The GUI has a field where you can enter your phrase expression. The <b>Source language</b> drop-down menu allows you to select the language of the word you have entered, or to have the language automatically detected. The <b>Target Language</b> drop-down menu allows you to select the target language.

The <b>'Translate'</b> button will translate the word or phrase you have entered into the target language. The application will also check the spelling of the phrase entered if a source language is given.
The <b>'Add to vocabulary list'</b> button allows you to add the entered phrase to a list and also checks for spelling mistakes. To save this list, press the <b>'Save vocabulary list'</b> button. After pressing the button, you can choose where you want to save the list and whether you want to save it as an Anki or Excel file.

To close the window press [x] in the top corner of the interface or th <b>'Quit'</b> button.

## Testing
To perform a unit test on the functions used, run pytest:
```console
$ pytest
```
You can also give the parameter 'key_path' in case you want to use a different DeepL key for your tests.
```console
$ pytest --keypath <path-to-the key-file> 
```
