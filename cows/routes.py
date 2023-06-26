from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

import cows.crud as crud
import cows.schemas as schemas

router = APIRouter()


@router.get("/cows/{id}")
async def get_one(id: int) -> schemas.Get:
    row = await crud.read_one(id)
    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"cow with id={id} not found",
        )
    return schemas.Get.from_row(row)


@router.get("/cows")
async def get_all(
    name: str = Query(None),
    sex: str = Query(None),
    birthdate: str = Query(None),
    condition: str = Query(None),
) -> list[schemas.Get]:
    # TODO pagination
    # TODO validate query params
    rows = await crud.read_all(
        name=name,
        sex=sex,
        birthdate=birthdate,
        condition=condition,
    )
    return [schemas.Get.from_row(row) for row in rows]


@router.post("/cows")
async def post(cow: schemas.Post) -> schemas.Get:
    cow_id = await crud.create(cow.flatten())
    return {**dict(cow), "id": cow_id}


@router.put("/cows/{cow_id}")
async def update(cow_id: int, update: schemas.Put) -> schemas.Get:
    await crud.update(cow_id, update.flatten())
    cow = await crud.read_one(cow_id)
    return schemas.Get.from_row(cow)


@router.delete(
    "/cows/{cow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(cow_id: int):
    await crud.delete(cow_id)
