from uuid import UUID

from pydantic import ValidationError
import pytest
from store.schemas.product import ProductIn
from tests.schemas.factories import product_data


def test_schemas_return_sucess():
    data = product_data()

    product = ProductIn.model_validate(data)

    assert product.name == "I5 2410M"
    assert isinstance(product.id, UUID)


def test_schemas_return_raise():
    data = {
        "name": "I5 2410M",
        "quantity": 100,
        "price": 83.0,
    }

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "I5 2410M", "quantity": 100, "price": 83.0},
        "url": "https://errors.pydantic.dev/2.7/v/missing",
    }
