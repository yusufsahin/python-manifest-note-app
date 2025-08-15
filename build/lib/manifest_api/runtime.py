from typing import Any, Dict, Optional, Tuple
from pydantic import BaseModel, Field, create_model
from datetime import datetime, date

TYPE_MAP = {
    "string": str,
    "text": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "date": date,
    "datetime": datetime,
}

def _pydantic_field(f: Dict[str, Any]) -> Tuple[str, tuple]:
    name = f["name"]
    typ = f.get("type", "string")
    py_type = TYPE_MAP.get(typ, str)

    required = f.get("required", False)
    default = None if not required else ...

    kwargs = {}
    if "minLength" in f: kwargs["min_length"] = f["minLength"]
    if "maxLength" in f: kwargs["max_length"] = f["maxLength"]
    if "minimum" in f:   kwargs["ge"] = f["minimum"]
    if "maximum" in f:   kwargs["le"] = f["maximum"]

    return name, (py_type, Field(default=default, **kwargs))

def make_models(entity: Dict[str, Any]) -> tuple[type[BaseModel], type[BaseModel], type[BaseModel]]:
    fields = dict(_pydantic_field(f) for f in entity["fields"])

    CreateModel = create_model(f"{entity['name'].title()}Create", **fields)  # type: ignore

    upd_fields = {}
    for k, (ann, fld) in fields.items():
        upd_fields[k] = (Optional[ann], Field(default=None))

    UpdateModel = create_model(f"{entity['name'].title()}Update", **upd_fields)  # type: ignore

    class BaseOut(BaseModel):
        id: int
        created_at: datetime
        updated_at: datetime
        model_config = {"from_attributes": True}

    OutModel = create_model(f"{entity['name'].title()}Out", __base__=BaseOut, **fields)  # type: ignore
    return CreateModel, UpdateModel, OutModel
