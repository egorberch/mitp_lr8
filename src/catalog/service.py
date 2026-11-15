"""Сервисный слой для управления каталогом учебных дисциплин."""

from typing import Dict, List, Optional

from src.catalog.models import CourseItem


class CatalogService:
    """Сервис учёта, фильтрации и агрегации учебных дисциплин."""

    def __init__(self) -> None:
        """Инициализирует пустое хранилище каталога дисциплин."""
        self._items: Dict[str, CourseItem] = {}

    def register_course(self, course: CourseItem) -> None:
        """Добавляет дисциплину в каталог с проверкой уникальности кода."""
        if course.code in self._items:
            raise ValueError(
                f"Дисциплина с кодом '{course.code}' уже зарегистрирована"
            )
        self._items[course.code] = course

    def get_by_code(self, code: str) -> Optional[CourseItem]:
        """Возвращает дисциплину по её уникальному коду или None."""
        return self._items.get(code)

    def list_courses(self) -> List[CourseItem]:
        """Возвращает список всех дисциплин, отсортированный по коду."""
        return [self._items[key] for key in sorted(self._items.keys())]

    def filter_by_min_credits(self, min_credits: int) -> List[CourseItem]:
        """Возвращает дисциплины с числом зачётных единиц не ниже порога."""
        return [
            item
            for item in self.list_courses()
            if item.credits >= min_credits
        ]

    def total_credits(self) -> int:
        """Вычисляет суммарное количество зачётных единиц по всему каталогу."""
        return sum(item.credits for item in self._items.values())

    def total_hours(self) -> int:
        """Вычисляет суммарное количество часов по всем дисциплинам."""
        return sum(item.hours for item in self._items.values())
