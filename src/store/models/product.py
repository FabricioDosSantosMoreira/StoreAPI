from store.schemas.product import ProductBase
from store.models.base import CreateBaseModel, UpdateBaseModel


class ProductCreateModel(ProductBase, CreateBaseModel):
    pass

class ProductUpdateModel(ProductBase, UpdateBaseModel):
    pass
