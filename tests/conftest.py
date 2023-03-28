def pytest_addoption(parser):
    """Get the path of the Deepl Key."""
    dirname = os.path.dirname(__file__)
    key_path = os.path.join(dirname, 'DeeplKey.txt')
    parser.addoption("--keypath", action="store", default=key_path)
