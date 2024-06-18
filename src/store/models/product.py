from store.schemas.product import ProductIn
from store.models.base import CreateBaseModel


class ProductModel(ProductIn, CreateBaseModel):
    pass
