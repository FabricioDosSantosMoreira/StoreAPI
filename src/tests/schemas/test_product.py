from pydantic import ValidationError

import pytest
from store.schemas.product import ProductCreateIn
from tests.factories import product_data


def test_schemas_return_sucess():

    product = ProductCreateIn.model_validate(product_data())

    assert product.name == "Intel Core i5 2410M"


def test_schemas_return_raise():
    
    data = {
        "name": "Intel Core i5 2410M",
        "quantity": 500,
        "price": 225.5,
    }
    with pytest.raises(ValidationError) as err:
        ProductCreateIn.model_validate(data)

    assert err.value.errors()[0]["input"] == {
        'name': 'Intel Core i5 2410M', 
        'quantity': 500, 
        'price': 225.5,
    }
