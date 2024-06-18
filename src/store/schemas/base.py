from datetime import datetime, timezone
import uuid
from pydantic import UUID4, BaseModel, Field
from pydantic_settings import SettingsConfigDict


class BaseSchemaMixin(BaseModel):
    model_config = SettingsConfigDict(arbitrary_types_allowed=True)
    # Configuração para permitir a atribuição de valores arbitários
    # ao usar pydantic

    id: UUID4 = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
