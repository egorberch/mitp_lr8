"""Задание №9 (средней сложности): Создать класс с property."""


class ProductInventoryItem:
    """Класс складской позиции с валидацией через декораторы property."""

    def __init__(
        self,
        title: str,
        unit_price: float,
        quantity: int = 0,
        discount_percent: float = 0.0,
    ) -> None:
        """Инициализирует товарную позицию через сеттеры свойств."""
        self._title = ""
        self._unit_price = 0.0
        self._quantity = 0
        self._discount_percent = 0.0

        self.title = title
        self.unit_price = unit_price
        self.quantity = quantity
        self.discount_percent = discount_percent

    @property
    def title(self) -> str:
        """Возвращает наименование товара."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Устанавливает наименование товара после очистки пробелов."""
        if not isinstance(value, str):
            raise TypeError("Наименование товара должно быть строкой")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Наименование товара не может быть пустым")
        self._title = cleaned

    @property
    def unit_price(self) -> float:
        """Возвращает базовую цену за единицу товара."""
        return self._unit_price

    @unit_price.setter
    def unit_price(self, value: float) -> None:
        """Проверяет и устанавливает положительную цену за единицу товара."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Цена товара должна быть числом")
        if value <= 0:
            raise ValueError("Цена за единицу должна быть строго больше нуля")
        self._unit_price = round(float(value), 2)

    @property
    def quantity(self) -> int:
        """Возвращает текущее количество единиц товара на складе."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Проверяет и устанавливает неотрицательный остаток на складе."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Количество товара должно быть целым числом")
        if value < 0:
            raise ValueError("Остаток на складе не может быть отрицательным")
        self._quantity = value

    @property
    def discount_percent(self) -> float:
        """Возвращает текущий процент скидки на товар."""
        return self._discount_percent

    @discount_percent.setter
    def discount_percent(self, value: float) -> None:
        """Устанавливает процент скидки в допустимом диапазоне [0, 90]."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Скидка должна быть числом")
        if not 0.0 <= float(value) <= 90.0:
            raise ValueError(
                "Скидка должна находиться в диапазоне от 0 до 90%"
            )
        self._discount_percent = round(float(value), 2)

    @discount_percent.deleter
    def discount_percent(self) -> None:
        """Сбрасывает процент скидки к нулевому значению."""
        self._discount_percent = 0.0

    @property
    def final_unit_price(self) -> float:
        """Вычисляемое свойство: цена единицы товара с учётом скидки."""
        multiplier = 1.0 - (self._discount_percent / 100.0)
        return round(self._unit_price * multiplier, 2)

    @property
    def total_inventory_cost(self) -> float:
        """Вычисляемое свойство: стоимость всей партии со скидкой."""
        return round(self.final_unit_price * self._quantity, 2)

    @property
    def is_in_stock(self) -> bool:
        """Вычисляемое свойство: признак наличия товара на складе."""
        return self._quantity > 0


def main() -> None:
    """Демонстрирует работу геттеров, сеттеров и вычисляемых свойств."""
    item = ProductInventoryItem(
        title="  SSD-накопитель NVMe 1TB  ",
        unit_price=8500.0,
        quantity=10,
        discount_percent=10.0,
    )
    print(f"Товар: '{item.title}'")
    print(
        f"Базовая цена: {item.unit_price:.2f} руб., "
        f"скидка: {item.discount_percent:.1f}%, "
        f"цена со скидкой: {item.final_unit_price:.2f} руб."
    )
    print(
        f"В наличии: {item.quantity} шт. (is_in_stock={item.is_in_stock}), "
        f"общая стоимость: {item.total_inventory_cost:.2f} руб."
    )

    item.discount_percent = 20.0
    if item.final_unit_price != 6800.0:
        raise RuntimeError("Некорректный пересчёт цены при изменении скидки")

    del item.discount_percent
    print(
        f"После сброса скидки (del item.discount_percent): "
        f"скидка={item.discount_percent:.1f}%, "
        f"цена={item.final_unit_price:.2f} руб."
    )


if __name__ == "__main__":
    main()
