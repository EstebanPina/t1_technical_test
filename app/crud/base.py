# app/crud/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from beanie import Document
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Document)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: Union[str, UUID]) -> Optional[ModelType]:
        if isinstance(id, UUID):
            id = str(id)
        return await self.model.find_one({"$or": [{"_id": id}, {"cliente_id": id}]})

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return await self.model.find().skip(skip).limit(limit).to_list()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict() if hasattr(obj_in, 'dict') else obj_in
        model_fields = self.model.__fields__
        
        # Buscar campos que terminen en '_id' y no estén en los datos de entrada
        for field_name, field in model_fields.items():
            if (field_name.endswith('_id') and 
                field_name not in obj_in_data and 
                field.default is None and 
                field.default_factory is None):
                from uuid import uuid4
                obj_in_data[field_name] = str(uuid4())
        
        db_obj = self.model(**obj_in_data)
        await db_obj.create()
        return db_obj

    async def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, 'dict') else obj_in
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db_obj.save()
        return db_obj

    async def remove(self, *, id: Union[str, UUID]) -> ModelType:
        if isinstance(id, UUID):
            id = str(id)
        obj = await self.model.find_one({"_id": id})
        if not obj:
            raise ValueError(f"{self.model.__name__} not found")
        await obj.delete()
        return obj