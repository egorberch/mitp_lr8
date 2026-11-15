"""Функции форматирования данных учебного каталога для отображения."""

from src.catalog.models import CourseItem


def format_course_line(course: CourseItem) -> str:
    """Форматирует объект дисциплины в информативную текстовую строку."""
    return (
        f"[{course.code}] {course.title} — "
        f"{course.credits} ЗЕТ ({course.hours} ак. ч.)"
    )
