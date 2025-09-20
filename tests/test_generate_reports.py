import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parse_csv_file import generate_student_report


def test_single_student_single_grande():

    data = [{"student_name": "Анна", "grade": "5.0"}]

    result = generate_student_report(data)
    assert len(result) == 1
    assert result[0]["student"] == "Анна"
    assert result[0]["average"] == 5.0


def test_multiple_student_one_grade():

    data = [
        {"student_name": "Анна", "grade": "5"},
        {"student_name": "Анна", "grade": "3.0"},
    ]

    result = generate_student_report(data)
    assert result[0]["average"] == 4.0


def test_ignore_empty_name():
    data = [{"student_name": "", "grade": "5"}, {"student_name": "Иван", "grade": "4"}]
    result = generate_student_report(data)
    assert result[0]["student"] == "Иван"


def test_empty_input():
    data = []
    result = generate_student_report(data)
    assert result == []


def test_rounding_to_two_decimals():  # Тест на округление до двух знаков
    data = [
        {"student_name": "Боб", "grade": "5"},
        {"student_name": "Боб", "grade": "4"},
        {"student_name": "Боб", "grade": "5"},
    ]
    result = generate_student_report(data)
    assert len(result) == 1
    assert result[0]["average"] == 4.67
