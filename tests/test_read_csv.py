import os
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parse_csv_file import read_csv_file


def test_read_one_file_simple():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        f.write("student_name,grade\nАнна,5\nИван,4")
        filename = f.name

    try:

        result = read_csv_file([filename])

        assert len(result) == 2

        assert result[0]["student_name"] == "Анна"
        assert result[0]["grade"] == "5"

        assert result[1]["student_name"] == "Иван"
        assert result[1]["grade"] == "4"

    finally:

        os.unlink(filename)
