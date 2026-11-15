"""Задание №5 (средней сложности): Структурировать проект (папка src)."""

from pathlib import Path
import sys
from typing import List

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.catalog import (  # noqa: E402
    CatalogService,
    CourseItem,
    format_course_line,
)


def verify_src_layout(project_root: Path) -> List[str]:
    """Проверяет наличие ключевых модулей внутри директории src/catalog."""
    expected_paths = [
        project_root / "src" / "__init__.py",
        project_root / "src" / "catalog" / "__init__.py",
        project_root / "src" / "catalog" / "models.py",
        project_root / "src" / "catalog" / "service.py",
        project_root / "src" / "catalog" / "formatter.py",
    ]
    missing = [
        str(path.relative_to(project_root))
        for path in expected_paths
        if not path.is_file()
    ]
    if missing:
        raise FileNotFoundError(
            f"Отсутствуют обязательные файлы структуры src: {missing}"
        )
    return [str(path.relative_to(project_root)) for path in expected_paths]


def main() -> None:
    """Демонстрирует работу пакета src/catalog и проверяет структуру папок."""
    verified_files = verify_src_layout(BASE_DIR)
    print("Проверена модульная структура проекта (src-layout):")
    for rel_file in verified_files:
        print(f"  + {rel_file}")

    catalog = CatalogService()
    sample_courses = [
        CourseItem("MITP-08", "Методы и технологии программирования", 5, 180),
        CourseItem(
            "PABD-06", "Программирование и администрирование БД", 4, 144
        ),
        CourseItem("TSISA-05", "Теория систем и системный анализ", 3, 108),
    ]
    for course in sample_courses:
        catalog.register_course(course)

    print("\nЗарегистрированные в пакете src.catalog дисциплины:")
    for course in catalog.list_courses():
        print(f"  {format_course_line(course)}")

    total_cred = catalog.total_credits()
    total_hrs = catalog.total_hours()
    print(f"\nИтого по учебному плану: {total_cred} ЗЕТ, {total_hrs} ак. ч.")
    if total_cred != 12 or total_hrs != 432:
        raise RuntimeError("Несовпадение контрольных сумм учебного плана")


if __name__ == "__main__":
    main()
