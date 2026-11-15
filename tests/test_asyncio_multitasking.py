"""Модульные тесты pytest для задания №7 повышенной сложности (asyncio)."""

import asyncio
import time
import pytest

from asyncio_multitasking import (
    execute_with_timeout,
    process_items_with_workers,
    run_concurrent_fetches,
)


def test_run_concurrent_fetches_speed_and_order() -> None:
    """Проверяет параллельное выполнение задач и сохранение порядка ответов."""
    specs = [
        ("node_a", 0.04, 10),
        ("node_b", 0.04, 20),
        ("node_c", 0.04, 30),
    ]
    start = time.perf_counter()
    results = asyncio.run(run_concurrent_fetches(specs, max_concurrent=3))
    elapsed = time.perf_counter() - start

    assert [r.source_name for r in results] == ["node_a", "node_b", "node_c"]
    assert sum(r.records_loaded for r in results) == 60
    assert elapsed < 0.11


def test_process_items_with_workers_queue() -> None:
    """Проверяет асинхронную обработку очереди пулом воркеров."""
    items = [1, 3, 5, 7, 9]
    output = asyncio.run(
        process_items_with_workers(items, worker_count=2, step_delay=0.005)
    )
    assert output == {1: 1, 3: 9, 5: 25, 7: 49, 9: 81}


def test_execute_with_timeout_behavior() -> None:
    """Проверяет обработку завершения и таймаута в asyncio.wait_for."""
    ok_res = asyncio.run(execute_with_timeout(0.005, 0.05))
    timeout_res = asyncio.run(execute_with_timeout(0.05, 0.005))
    assert ok_res == "completed"
    assert timeout_res == "timed_out"


def test_asyncio_validation_errors() -> None:
    """Проверяет валидацию некорректных параметров конкурентности."""
    with pytest.raises(ValueError):
        asyncio.run(run_concurrent_fetches([], max_concurrent=0))
    with pytest.raises(ValueError):
        asyncio.run(process_items_with_workers([1, 2], worker_count=0))
