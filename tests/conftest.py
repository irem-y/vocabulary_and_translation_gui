"""
Configuration for pytest.

The function allows the user to enter a Path to the file where the DeepL
Authentication Key is stored. This Key will be used in the test
functions that test translation funcitonalities.
"""
import os


def pytest_addoption(parser):
    """Get the path of the Deepl Key."""
    dirname = os.path.dirname(__file__)
    key_path = os.path.abspath(os.path.join(dirname, "..", "src",
                                            "vocabulary_and_translation_gui",
                                            "resources",
                                            "deepl_key.txt")
                               )
    parser.addoption("--keypath", action="store", default=key_path)
