from decimal import Decimal
from typing import List
from uuid import UUID

import pytest
from store.schemas.product import ProductOut
from store.usecases.product import product_usecase
from store.core.exception import NotFoundException


async def test_usecases_create_should_return_sucess(product_in):

    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Intel Core i5 2410M"


async def test_usecases_get_should_return_sucess(product_inserted):

    result = await product_usecase.get_by_id(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Intel Core i5 2410M"


async def test_usecases_get_should_return_not_found():

    message = "Product not found with filter: UUID('c711f373-c9cf-4b69-9249-9c755f208d6c')"

    with pytest.raises(NotFoundException) as err:
        await product_usecase.get_by_id(id=UUID("c711f373-c9cf-4b69-9249-9c755f208d6c"))
    assert err.value.message == message


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_sucess():
    result = await product_usecase.get_all()

    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_sucess(product_up, product_inserted):

    product_up.price = Decimal("809.9")
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductOut)
    assert str(result.price) == "809.9"
    assert result.id == product_inserted.id


async def test_usecases_delete_should_return_sucess(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


async def test_usecases_delete_should_return_not_found():

    message = "Product not found with filter: UUID('c711f373-c9cf-4b69-9249-9c755f208d6c')"

    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID("c711f373-c9cf-4b69-9249-9c755f208d6c"))

    assert err.value.message == message

