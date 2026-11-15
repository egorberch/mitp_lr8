"""Задание №3 (повышенная сложность): Использовать шаблон Repository."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
import sqlite3
from typing import Dict, List, Optional


@dataclass
class TaskEntity:
    """Доменная сущность проектной задачи."""

    id: Optional[int]
    title: str
    assignee: str
    completed: bool = False


class AbstractTaskRepository(ABC):
    """Абстрактный интерфейс репозитория для работы с задачами."""

    @abstractmethod
    def add(self, task: TaskEntity) -> TaskEntity:
        """Сохраняет новую задачу в хранилище и назначает ей ID."""

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        """Возвращает задачу по её идентификатору или None."""

    @abstractmethod
    def list_all(self) -> List[TaskEntity]:
        """Возвращает список всех задач, отсортированный по ID."""

    @abstractmethod
    def list_by_assignee(self, assignee: str) -> List[TaskEntity]:
        """Возвращает список задач, назначенных указанному исполнителю."""

    @abstractmethod
    def update(self, task: TaskEntity) -> TaskEntity:
        """Обновляет существующую задачу в хранилище."""

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Удаляет задачу по идентификатору и возвращает статус удаления."""


class InMemoryTaskRepository(AbstractTaskRepository):
    """Реализация репозитория задач в оперативной памяти (для unit-тестов)."""

    def __init__(self) -> None:
        """Инициализирует пустой словарь хранения и счётчик идентификаторов."""
        self._storage: Dict[int, TaskEntity] = {}
        self._next_id: int = 1

    def add(self, task: TaskEntity) -> TaskEntity:
        """Сохраняет копию задачи в памяти с новым идентификатором."""
        assigned_id = self._next_id
        self._next_id += 1
        saved = replace(task, id=assigned_id)
        self._storage[assigned_id] = saved
        return replace(saved)

    def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        """Возвращает копию задачи по ID или None, если она не найдена."""
        found = self._storage.get(task_id)
        return replace(found) if found is not None else None

    def list_all(self) -> List[TaskEntity]:
        """Возвращает список копий всех задач по возрастанию ID."""
        return [
            replace(self._storage[key]) for key in sorted(self._storage.keys())
        ]

    def list_by_assignee(self, assignee: str) -> List[TaskEntity]:
        """Возвращает задачи указанного исполнителя."""
        return [
            replace(item)
            for item in self.list_all()
            if item.assignee == assignee
        ]

    def update(self, task: TaskEntity) -> TaskEntity:
        """Обновляет запись задачи в словаре по её идентификатору."""
        if task.id is None or task.id not in self._storage:
            raise KeyError(f"Задача с ID={task.id} не найдена в репозитории")
        updated = replace(task)
        self._storage[task.id] = updated
        return replace(updated)

    def delete(self, task_id: int) -> bool:
        """Удаляет задачу из словаря по ключу."""
        return self._storage.pop(task_id, None) is not None


class SQLiteTaskRepository(AbstractTaskRepository):
    """Реализация репозитория задач поверх реляционной СУБД SQLite."""

    def __init__(self, db_path: str = ":memory:") -> None:
        """Открывает соединение с SQLite и создаёт таблицу tasks."""
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Создаёт таблицу для хранения сущностей TaskEntity."""
        query = """
        CREATE TABLE IF NOT EXISTS repository_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            assignee TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
        with self.connection:
            self.connection.execute(query)

    @staticmethod
    def _row_to_entity(row: sqlite3.Row) -> TaskEntity:
        """Преобразует строку sqlite3.Row в объект доменной модели."""
        return TaskEntity(
            id=int(row["id"]),
            title=str(row["title"]),
            assignee=str(row["assignee"]),
            completed=bool(row["completed"]),
        )

    def add(self, task: TaskEntity) -> TaskEntity:
        """Вставляет новую запись в таблицу SQLite и возвращает сущность."""
        query = """
        INSERT INTO repository_tasks (title, assignee, completed)
        VALUES (?, ?, ?)
        """
        with self.connection:
            cursor = self.connection.execute(
                query, (task.title, task.assignee, int(task.completed))
            )
            new_id = int(cursor.lastrowid or 0)
        return replace(task, id=new_id)

    def get_by_id(self, task_id: int) -> Optional[TaskEntity]:
        """Находит задачу в таблице по первичному ключу."""
        query = """
        SELECT id, title, assignee, completed
        FROM repository_tasks
        WHERE id = ?
        """
        row = self.connection.execute(query, (task_id,)).fetchone()
        return self._row_to_entity(row) if row is not None else None

    def list_all(self) -> List[TaskEntity]:
        """Извлекает все задачи из таблицы с сортировкой по ID."""
        query = """
        SELECT id, title, assignee, completed
        FROM repository_tasks
        ORDER BY id ASC
        """
        rows = self.connection.execute(query).fetchall()
        return [self._row_to_entity(row) for row in rows]

    def list_by_assignee(self, assignee: str) -> List[TaskEntity]:
        """Извлекает все задачи конкретного исполнителя."""
        query = """
        SELECT id, title, assignee, completed
        FROM repository_tasks
        WHERE assignee = ?
        ORDER BY id ASC
        """
        rows = self.connection.execute(query, (assignee,)).fetchall()
        return [self._row_to_entity(row) for row in rows]

    def update(self, task: TaskEntity) -> TaskEntity:
        """Обновляет поля существующей задачи в БД SQLite."""
        if task.id is None:
            raise KeyError("Невозможно обновить задачу без идентификатора")
        query = """
        UPDATE repository_tasks
        SET title = ?, assignee = ?, completed = ?
        WHERE id = ?
        """
        with self.connection:
            cursor = self.connection.execute(
                query,
                (task.title, task.assignee, int(task.completed), task.id),
            )
            if cursor.rowcount == 0:
                raise KeyError(f"Задача с ID={task.id} не найдена в БД")
        return replace(task)

    def delete(self, task_id: int) -> bool:
        """Удаляет строку задачи из таблицы по её ID."""
        query = "DELETE FROM repository_tasks WHERE id = ?"
        with self.connection:
            cursor = self.connection.execute(query, (task_id,))
            return cursor.rowcount > 0

    def close(self) -> None:
        """Закрывает соединение с базой данных SQLite."""
        self.connection.close()


class TaskService:
    """Сервис управления задачами, зависящий от абстракции репозитория."""

    def __init__(self, repository: AbstractTaskRepository) -> None:
        """Принимает реализацию репозитория через внедрение зависимостей."""
        self._repo = repository

    def create_task(self, title: str, assignee: str) -> TaskEntity:
        """Проверяет входные данные и создаёт задачу через репозиторий."""
        clean_title = title.strip()
        clean_assignee = assignee.strip()
        if not clean_title or not clean_assignee:
            raise ValueError("Название задачи и исполнитель обязательны")
        return self._repo.add(
            TaskEntity(id=None, title=clean_title, assignee=clean_assignee)
        )

    def mark_completed(self, task_id: int) -> TaskEntity:
        """Переводит задачу в статус выполненной."""
        existing = self._repo.get_by_id(task_id)
        if existing is None:
            raise KeyError(f"Задача с ID={task_id} не существует")
        existing.completed = True
        return self._repo.update(existing)


def run_demo_with_repo(
    label: str, repo: AbstractTaskRepository
) -> List[TaskEntity]:
    """Выполняет единый сценарий бизнес-логики на переданном репозитории."""
    service = TaskService(repo)
    first = service.create_task("Спроектировать слой Repository", "Егор")
    second = service.create_task("Написать модульные тесты pytest", "Егор")
    third = service.create_task("Настроить сборку пакета", "Данила")

    if first.id is not None:
        service.mark_completed(first.id)
    if third.id is not None:
        repo.delete(third.id)

    tasks = repo.list_all()
    print(f"\nХранилище [{label}] — активных записей: {len(tasks)}")
    for item in tasks:
        state = "Готово" if item.completed else "В работе"
        print(
            f"  [ID={item.id}] {item.title} "
            f"(исполнитель: {item.assignee}, статус: {state})"
        )
    if len(tasks) != 2 or second.id is None:
        raise RuntimeError("Нарушена консистентность операций репозитория")
    return tasks


def main() -> None:
    """Демонстрирует взаимозаменяемость InMemory и SQLite репозиториев."""
    print("Демонстрация шаблона проектирования Repository:")
    mem_repo = InMemoryTaskRepository()
    run_demo_with_repo("InMemoryTaskRepository", mem_repo)

    sqlite_repo = SQLiteTaskRepository(":memory:")
    try:
        run_demo_with_repo("SQLiteTaskRepository", sqlite_repo)
    finally:
        sqlite_repo.close()


if __name__ == "__main__":
    main()
