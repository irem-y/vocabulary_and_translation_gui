from __future__ import annotations

import vocabulary_and_translation_gui


def test_import():
    assert hasattr(vocabulary_and_translation_gui, "__version__")
