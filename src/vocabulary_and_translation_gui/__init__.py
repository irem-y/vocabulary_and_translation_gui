"""This contains the main namespace of vocabulary_and_translation_gui."""
# Import the version from _version.py which is dynamically created by
# setuptools-scmcc when the project is installed with ``pip install -e .``.
# Do not put it into version control!
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"


__all__ = ["__version__"]
