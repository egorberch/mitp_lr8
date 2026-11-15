"""Модульные тесты pytest для задания №9 средней сложности (property)."""

import pytest

from property_class import ProductInventoryItem


def test_product_properties_and_computed_fields() -> None:
    """Проверяет чтение, запись, удаление и расчётные свойства товара."""
    item = ProductInventoryItem("  Монитор 27 дюймов  ", 25000.0, 4, 10.0)
    assert item.title == "Монитор 27 дюймов"
    assert item.unit_price == pytest.approx(25000.0)
    assert item.quantity == 4
    assert item.discount_percent == pytest.approx(10.0)
    assert item.final_unit_price == pytest.approx(22500.0)
    assert item.total_inventory_cost == pytest.approx(90000.0)
    assert item.is_in_stock is True

    item.quantity = 0
    assert item.is_in_stock is False

    del item.discount_percent
    assert item.discount_percent == pytest.approx(0.0)
    assert item.final_unit_price == pytest.approx(25000.0)


def test_product_property_setters_validation() -> None:
    """Проверяет защиту сеттеров от некорректных значений и типов."""
    item = ProductInventoryItem("Клавиатура", 3500.0, 2, 0.0)

    with pytest.raises(ValueError):
        item.title = "   "
    with pytest.raises(ValueError):
        item.unit_price = -500.0
    with pytest.raises(ValueError):
        item.quantity = -1
    with pytest.raises(ValueError):
        item.discount_percent = 95.0
    with pytest.raises(TypeError):
        item.quantity = True
