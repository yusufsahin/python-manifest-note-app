from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from .db import get_db
from .models import Record

def build_router(entity: Dict[str, Any], CreateModel, UpdateModel, OutModel) -> APIRouter:
    name = entity["name"]
    plural = entity.get("plural", name + "s")
    router = APIRouter(prefix=f"/api/{plural}", tags=[plural])

    search_fields = [f["name"] for f in entity["fields"] if f.get("type") in ("string", "text")]

    @router.get("", response_model=List[OutModel])
    def list_items(
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=200),
        q: Optional[str] = Query(None, description="Simple contains search in string/text fields"),
        db: Session = Depends(get_db),
    ):
        stmt = select(Record).where(Record.type == name)

        if q and search_fields:
            pattern = f"%{q}%"
            filters = [Record.data[field].as_string().ilike(pattern) for field in search_fields]
            stmt = stmt.where(or_(*filters))

        stmt = stmt.order_by(Record.id.desc()).offset(skip).limit(limit)
        rows = db.execute(stmt).scalars().all()
        return [to_out(r) for r in rows]

    @router.post("", response_model=OutModel, status_code=status.HTTP_201_CREATED)
    def create_item(payload: CreateModel, db: Session = Depends(get_db)):
        rec = Record(type=name, data=payload.model_dump())
        db.add(rec); db.commit(); db.refresh(rec)
        return to_out(rec)

    @router.get("/{item_id}", response_model=OutModel)
    def get_item(item_id: int, db: Session = Depends(get_db)):
        rec = db.get(Record, item_id)
        if not rec or rec.type != name:
            raise HTTPException(404, "Item not found")
        return to_out(rec)

    @router.put("/{item_id}", response_model=OutModel)
    def update_item(item_id: int, payload: UpdateModel, db: Session = Depends(get_db)):
        rec = db.get(Record, item_id)
        if not rec or rec.type != name:
            raise HTTPException(404, "Item not found")
        data = rec.data.copy()
        for k, v in payload.model_dump(exclude_unset=True, exclude_none=False).items():
            data[k] = v
        rec.data = data
        db.add(rec); db.commit(); db.refresh(rec)
        return to_out(rec)

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        rec = db.get(Record, item_id)
        if not rec or rec.type != name:
            raise HTTPException(404, "Item not found")
        db.delete(rec); db.commit()
        return None

    def to_out(rec: Record):
        return {"id": rec.id, **rec.data, "created_at": rec.created_at, "updated_at": rec.updated_at}

    return router
