## Берченёв Егор Константинович, группа 220042-11, вариант 3, лабораторная №8

## "Экосистемы Python, их использование"

## Задания варианта 3:

Средней сложности:
- №3 - Написать простую функцию и тест pytest (`simple_function_pytest.py`, `tests/test_simple_function.py`)
- №5 - Структурировать проект (папка src) (`project_structure.py`, `src/catalog/`, `pyproject.toml`)
- №9 - Создать класс с property (`property_class.py`, `tests/test_property_class.py`)

Повышенной сложности:
- №3 - Использовать шаблон Repository (`repository_pattern.py`, `tests/test_repository_pattern.py`)
- №7 - Использовать asyncio для многозадачности (`asyncio_multitasking.py`, `tests/test_asyncio_multitasking.py`)

## Инструкция по запуску:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python simple_function_pytest.py
python project_structure.py
python property_class.py
python repository_pattern.py
python asyncio_multitasking.py

pytest
```

Все скрипты и модульные тесты оформлены по PEP8 и проверены FLAKE8 (`python -m flake8 .`).
