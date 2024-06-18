from tests.factories import product_data
from fastapi import status


async def test_controller_create_should_return_sucess(client, products_url):
    response = await client.post(url=products_url, json=product_data())

    assert response.status_code == status.HTTP_201_CREATED
