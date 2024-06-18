from typing import List

import pytest
from tests.factories import product_data
from fastapi import status


async def test_controller_create_should_return_sucess(client, products_url):
    response = await client.post(url=products_url, json=product_data())

    content = response.json()

    del content["id"]
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "I5 2410M",
        "quantity": 100,
        "price": "80.0",
        "status": True,
    }


async def test_controller_get_should_return_sucess(
    client, products_url, product_inserted
):
    response = await client.get(url=f"{products_url}{product_inserted.id}")

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "id": str(product_inserted.id),
        "name": "I5 2410M",
        "quantity": 100,
        "price": "80.0",
        "status": True,
    }


async def test_controller_get_should_return_not_found(
    client, products_url, product_inserted
):
    response = await client.get(
        url=f"{products_url}c711f373-c9cf-4b69-9249-9c755f208d6c"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json()["detail"]
        == "Product not found with filter: UUID('c711f373-c9cf-4b69-9249-9c755f208d6c')"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_sucess(client, products_url):
    response = await client.get(url=products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)

    assert len(response.json()) > 1


async def test_controller_patch_should_return_sucess(
    client, products_url, product_inserted
):
    response = await client.patch(
        url=f"{products_url}{product_inserted.id}",
        json={"quantity": 10, "price": "150.0"},
    )

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "I5 2410M",
        "quantity": 10,
        "price": "150.0",
        "status": True,
    }


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(url=f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        url=f"{products_url}c711f373-c9cf-4b69-9249-9c755f208d6c"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json()["detail"]
        == "Product not found with filter: UUID('c711f373-c9cf-4b69-9249-9c755f208d6c')"
    )
