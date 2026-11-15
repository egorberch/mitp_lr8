"""Пакет управления учебным каталогом дисциплин."""

from src.catalog.formatter import format_course_line
from src.catalog.models import CourseItem
from src.catalog.service import CatalogService

__all__ = [
    "CatalogService",
    "CourseItem",
    "format_course_line",
]
