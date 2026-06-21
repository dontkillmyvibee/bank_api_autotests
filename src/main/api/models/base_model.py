from pydantic import BaseModel, ConfigDict


class BaseModel(BaseModel):
    ...

class CamelCaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)