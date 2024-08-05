import datetime
from unittest import mock

import pytest

from app import main


@pytest.fixture
def products() -> list:
    return [
        {
            "name": "salmon",
            "expiration_date": datetime.date(2022, 2, 10),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": datetime.date(2022, 2, 5),
            "price": 120
        },
        {
            "name": "duck",
            "expiration_date": datetime.date(2022, 2, 1),
            "price": 160
        }
    ]


@pytest.mark.parametrize(
    ("current_date", "expected_products"),
    [
        (
            datetime.date(2022, 2, 11),
            ["salmon", "chicken", "duck"]
        ),
        (
            datetime.date(2022, 1, 31),
            []
        ),
        (
            datetime.date(2022, 2, 5),
            ["duck"]
        )
    ],
    ids=[
        "if all products are expired",
        "if all products are not expired",
        "if some products are expired and some not"
    ]
)
@mock.patch(f'{main.__name__}.datetime', wraps=datetime)
def test_should_return_correct_list(
    mocked_today: mock.Mock,
    products: list,
    current_date: datetime.date,
    expected_products: list
) -> None:
    mocked_today.date.today.return_value = current_date

    assert main.outdated_products(products) == expected_products
