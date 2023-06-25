from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from cows.models import db_cow_create
from cows.models import db_cow_delete
from cows.models import db_cow_get_list
from cows.models import db_cow_get_one
from cows.schemas import CowSchemaGet
from cows.schemas import CowSchemaPost

router = APIRouter()


@router.get("/cows/{id}")
async def cows_get_one(id: int) -> CowSchemaGet:
    row = await db_cow_get_one(id)
    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"cow with id={id} not found",
        )
    return CowSchemaGet.from_row(row)


@router.delete(
    "/cows/{cow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cows_delete(cow_id: int):
    await db_cow_delete(cow_id)


@router.get("/cows")
async def cows_get_list() -> list[CowSchemaGet]:
    rows = await db_cow_get_list()
    return [CowSchemaGet.from_row(row) for row in rows]


@router.post("/cows")
async def cows_post(cow: CowSchemaPost):
    cow_id = await db_cow_create(cow)
    return {**dict(cow), "id": cow_id}


# @router.put('/cows/{cow_id}')
# def update_cow(cow_id: int, cow_data:
#                 CowUpdate, db: Session = Depends(cows.main.db)):
#     cow = db.query(Cow).get(cow_id)
#     if cow:
#         for field, value in cow_data.dict(exclude_unset=True).items():
#             setattr(cow, field, value)
#         db.commit()
#         db.refresh(cow)
#         return cow
#     else:
#         return {"message": "Cow not found"}rou
