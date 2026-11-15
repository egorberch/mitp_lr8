"""Модульные тесты pytest для задания №5 средней сложности (папка src)."""

from pathlib import Path
import pytest

from project_structure import BASE_DIR, verify_src_layout
from src.catalog import CatalogService, CourseItem, format_course_line


def test_verify_src_layout_files_exist() -> None:
    """Проверяет наличие всех файлов пакета в директории src/catalog."""
    files = verify_src_layout(BASE_DIR)
    assert len(files) == 5
    assert "src/catalog/models.py" in [Path(p).as_posix() for p in files]


def test_course_item_validation() -> None:
    """Проверяет валидацию доменной модели CourseItem."""
    course = CourseItem("CS-101", "Алгоритмы и структуры данных", 4, 144)
    assert format_course_line(course) == (
        "[CS-101] Алгоритмы и структуры данных — 4 ЗЕТ (144 ак. ч.)"
    )
    with pytest.raises(ValueError):
        CourseItem("", "Пустой код", 3, 108)
    with pytest.raises(ValueError):
        CourseItem("CS-102", "Некорректные часы", 3, 0)


def test_catalog_service_operations() -> None:
    """Проверяет регистрацию, поиск, фильтрацию и подсчёт сумм в каталоге."""
    service = CatalogService()
    c1 = CourseItem("B-02", "Базы данных", 4, 144)
    c2 = CourseItem("A-01", "Архитектура ПО", 5, 180)
    service.register_course(c1)
    service.register_course(c2)

    assert service.get_by_code("A-01") == c2
    assert service.get_by_code("UNKNOWN") is None
    assert [c.code for c in service.list_courses()] == ["A-01", "B-02"]
    assert len(service.filter_by_min_credits(5)) == 1
    assert service.total_credits() == 9
    assert service.total_hours() == 324

    with pytest.raises(ValueError):
        service.register_course(c1)
