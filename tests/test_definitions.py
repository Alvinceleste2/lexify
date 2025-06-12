import pytest

from definitions import read_words, InputFileParsingError

TEMP_PATH = "test_temp/"


def test_input_parse_1(tmp_path):

    f = tmp_path / "test.txt"
    f.write_text("a(")

    with pytest.raises(InputFileParsingError) as e:
        read_words(f)

    assert str(e.value) == "Parenthesis are not balanced."
