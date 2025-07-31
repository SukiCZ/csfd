import unicodedata


def normalize(text: str) -> str:
    """
    Normalize the input text by removing diacritical marks (accents) from characters.
    :param text: str
        The text to normalize.
    :return: str
        The normalized text with diacritical marks removed.
    """
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")
