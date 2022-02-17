from pydantic import BaseModel


class CoreModel(BaseModel):
    pass


class ResponseModelMixin(BaseModel):
    id: int
