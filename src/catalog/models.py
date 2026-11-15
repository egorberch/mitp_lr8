"""Доменные модели учебного каталога дисциплин."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CourseItem:
    """Неизменяемая модель учебной дисциплины в каталоге."""

    code: str
    title: str
    credits: int
    hours: int

    def __post_init__(self) -> None:
        """Проверяет корректность полей дисциплины после инициализации."""
        if not self.code.strip():
            raise ValueError("Код дисциплины не может быть пустым")
        if not self.title.strip():
            raise ValueError("Название дисциплины не может быть пустым")
        if self.credits <= 0:
            raise ValueError("Число зачётных единиц должно быть положительным")
        if self.hours <= 0:
            raise ValueError("Количество академических часов должно быть > 0")
