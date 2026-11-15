"""Задание №7 (повышенная сложность): Асинхронная многозадачность asyncio."""

import asyncio
from dataclasses import dataclass
import time
from typing import Dict, List, Sequence, Tuple


@dataclass(frozen=True)
class TaskResult:
    """Результат выполнения асинхронной операции загрузки ресурса."""

    source_name: str
    records_loaded: int
    duration_sec: float


async def simulate_io_fetch(
    source_name: str, delay_sec: float, records_count: int
) -> TaskResult:
    """Имитирует асинхронный сетевой запрос с заданной задержкой."""
    if delay_sec < 0:
        raise ValueError("Время задержки не может быть отрицательным")
    start_ts = time.perf_counter()
    await asyncio.sleep(delay_sec)
    elapsed = round(time.perf_counter() - start_ts, 4)
    return TaskResult(
        source_name=source_name,
        records_loaded=records_count,
        duration_sec=elapsed,
    )


async def run_concurrent_fetches(
    specs: Sequence[Tuple[str, float, int]], max_concurrent: int = 3
) -> List[TaskResult]:
    """Выполняет группу корутин конкурентно с ограничением через Semaphore."""
    if max_concurrent <= 0:
        raise ValueError("Лимит конкурентности должен быть больше нуля")
    semaphore = asyncio.Semaphore(max_concurrent)

    async def _bounded_fetch(
        name: str, delay: float, count: int
    ) -> TaskResult:
        async with semaphore:
            return await simulate_io_fetch(name, delay, count)

    coroutines = [
        _bounded_fetch(name, delay, count) for name, delay, count in specs
    ]
    results = await asyncio.gather(*coroutines)
    return list(results)


async def process_items_with_workers(
    numbers: Sequence[int], worker_count: int = 3, step_delay: float = 0.01
) -> Dict[int, int]:
    """Обрабатывает очередь задач пулом асинхронных воркеров через Queue."""
    if worker_count <= 0:
        raise ValueError("Количество воркеров должно быть положительным")

    queue: asyncio.Queue[int] = asyncio.Queue()
    results: Dict[int, int] = {}

    for number in numbers:
        queue.put_nowait(number)

    async def _worker() -> None:
        while True:
            current = await queue.get()
            try:
                await asyncio.sleep(step_delay)
                results[current] = current * current
            finally:
                queue.task_done()

    workers = [
        asyncio.create_task(_worker()) for _ in range(worker_count)
    ]
    try:
        await queue.join()
    finally:
        for worker_task in workers:
            worker_task.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

    return {num: results[num] for num in numbers}


async def execute_with_timeout(delay_sec: float, timeout_sec: float) -> str:
    """Запускает корутину с контролем таймаута через asyncio.wait_for."""
    try:
        await asyncio.wait_for(
            asyncio.sleep(delay_sec), timeout=timeout_sec
        )
        return "completed"
    except asyncio.TimeoutError:
        return "timed_out"


async def async_main() -> None:
    """Запускает демонстрацию конкурентного выполнения задач на asyncio."""
    sources: List[Tuple[str, float, int]] = [
        ("users_service", 0.05, 120),
        ("orders_service", 0.06, 340),
        ("payments_service", 0.04, 215),
        ("analytics_service", 0.05, 890),
    ]
    sequential_estimate = sum(item[1] for item in sources)

    start_time = time.perf_counter()
    results = await run_concurrent_fetches(sources, max_concurrent=4)
    wall_time = time.perf_counter() - start_time

    print("1. Конкурентная загрузка из 4 микросервисов (asyncio.gather):")
    for res in results:
        print(
            f"   Источник {res.source_name}: {res.records_loaded} записей "
            f"(время задачи: {res.duration_sec:.3f} с)"
        )
    print(
        f"   Суммарное время последовательно: ~{sequential_estimate:.2f} с | "
        f"Фактическое время конкурентно: {wall_time:.3f} с"
    )

    numbers = [2, 4, 6, 8, 10, 12]
    squared_map = await process_items_with_workers(
        numbers, worker_count=3, step_delay=0.01
    )
    print(f"\n2. Обработка очереди воркерами (asyncio.Queue): {squared_map}")

    fast_status = await execute_with_timeout(0.01, 0.10)
    slow_status = await execute_with_timeout(0.10, 0.02)
    print(
        f"\n3. Контроль времени выполнения (asyncio.wait_for): "
        f"быстрая задача='{fast_status}', долгая задача='{slow_status}'"
    )


def main() -> None:
    """Точка входа для запуска асинхронного сценария."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
