"""Модульные тесты pytest для задания №3 повышенной сложности (Repository)."""

from typing import Generator
import pytest

from repository_pattern import (
    AbstractTaskRepository,
    InMemoryTaskRepository,
    SQLiteTaskRepository,
    TaskEntity,
    TaskService,
)


@pytest.fixture(params=["memory", "sqlite"])
def task_repo(
    request: pytest.FixtureRequest,
) -> Generator[AbstractTaskRepository, None, None]:
    """Фикстура, предоставляющая обе реализации репозитория задач."""
    if request.param == "memory":
        repo: AbstractTaskRepository = InMemoryTaskRepository()
        yield repo
    else:
        sqlite_repo = SQLiteTaskRepository(":memory:")
        try:
            yield sqlite_repo
        finally:
            sqlite_repo.close()


def test_repository_crud_lifecycle(
    task_repo: AbstractTaskRepository,
) -> None:
    """Проверяет полный цикл CRUD для реализаций AbstractTaskRepository."""
    created = task_repo.add(
        TaskEntity(id=None, title="Подготовить отчёт", assignee="Егор")
    )
    assert created.id is not None

    loaded = task_repo.get_by_id(created.id)
    assert loaded is not None
    assert loaded.title == "Подготовить отчёт"
    assert loaded.completed is False

    loaded.completed = True
    loaded.title = "Подготовить итоговый отчёт"
    task_repo.update(loaded)

    updated = task_repo.get_by_id(created.id)
    assert updated is not None
    assert updated.completed is True
    assert updated.title == "Подготовить итоговый отчёт"

    assert len(task_repo.list_by_assignee("Егор")) == 1
    assert task_repo.delete(created.id) is True
    assert task_repo.delete(created.id) is False
    assert task_repo.get_by_id(created.id) is None


def test_task_service_business_rules(
    task_repo: AbstractTaskRepository,
) -> None:
    """Проверяет работу сервисного слоя поверх абстракции репозитория."""
    service = TaskService(task_repo)
    task = service.create_task("  Настроить CI  ", "  Егор  ")
    assert task.id is not None
    assert task.title == "Настроить CI"

    completed = service.mark_completed(task.id)
    assert completed.completed is True

    with pytest.raises(ValueError):
        service.create_task("   ", "Егор")
    with pytest.raises(KeyError):
        service.mark_completed(9999)
