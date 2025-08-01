from movies.utils import normalize


def test_normalize():
    # Test with various accented characters
    assert normalize("café") == "cafe"
    assert normalize("résumé") == "resume"
    assert normalize("naïve") == "naive"
    assert normalize("Zürich") == "Zurich"

    # Test with empty string
    assert normalize("") == ""

    # Test with no accented characters
    assert normalize("hello world") == "hello world"

    # Test with mixed accented and non-accented characters
    assert normalize("Déjà vu") == "Deja vu"

    # Test with characters from different languages
    assert normalize("piñata ñandú") == "pinata nandu"
    assert normalize("škola") == "skola"
    assert normalize("červený") == "cerveny"
