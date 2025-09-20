import argparse
import csv
import sys
from tabulate import tabulate


def read_csv_file(file_paths):
    result_students = []
    for file_path in file_paths:
        try:
            with open(file_path, encoding="utf-8", newline="") as a:
                reader = csv.DictReader(a)
                for row in reader:
                    result_students.append(row)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден, пожалуйста проверьте наличие файла! ")
            sys.exit(1)
    return result_students


def generate_student_report(data):
    result_list = []
    student_grades = {}
    for row in data:
        name = row.get("student_name")
        if not name or not isinstance(name, str):
            continue
        grade = row.get("grade")
        if not grade:
            continue
        try:
            grade = float(grade)
        except (ValueError, TypeError):
            continue
        if name not in student_grades:
            student_grades[name] = []
        student_grades[name].append(grade)
    for name, grade_list in student_grades.items():
        average = sum(grade_list) / len(grade_list)
        average = round(average, 2)  # Для точности в выводе до 2х знаков
        result_list.append({"student": name, "average": average})
    result_list.sort(key=lambda x: x["average"], reverse=True)
    return result_list

REPORTS = {
    "student-performance": generate_student_report,
    # сюда можно будет добавлять новые — функции для отчетов
}

def main():
    # Создаем обьект парсера аргументов скрипта и название отчета
    parser = argparse.ArgumentParser(
        description="Скрипт для генерации отчета по успеваимости студентов"
    )
    parser.add_argument(
        "--files",
        nargs="+",  # принимает 1 или более аргументов
        required=True,  # обязательный
        help="Список CSV файлов с данными по успеваемости",
    )
    parser.add_argument(
        "--report", required=True, help="Название отчета - student-performance"
    )
    args = parser.parse_args()
        
    if args.report not in REPORTS:
        print(f"Отчёт '{args.report}' не поддерживается. Доступные: {', '.join(REPORTS.keys())}")
        sys.exit(1)

    report_func = REPORTS[args.report] # Берем функцию из нашего словаря с функциями

    data = read_csv_file(args.files)
    
    report_data = report_func(data)

    table = tabulate(report_data, headers="keys", tablefmt="grid")
    print(table)


if __name__ == "__main__":
    main()
