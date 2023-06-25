from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import validator


class BaseSchema(BaseModel):
    class Config:
        validate_assignment = True

    @validator("*")
    def remove_timezone(cls, value):
        # Removing timezones is so that openapi docs work.
        # A production implementation would handle timezones
        if isinstance(value, datetime):
            return value.replace(tzinfo=None)
        return value


class _CowSchemaWeight(BaseSchema):
    mass_kg: int
    last_measured: datetime


class _CowSchemaMilkProduction(BaseSchema):
    last_milk: datetime
    cron_schedule: str
    amount_l: int


class _CowSchemaFeeding(BaseSchema):
    amount_kg: int
    cron_schedule: str
    last_measured: datetime


class CowSchemaDelete(BaseSchema):
    id: int


class CowSchemaBase(BaseSchema):
    name: str
    sex: str
    birthdate: datetime
    condition: str
    weight: _CowSchemaWeight
    feeding: _CowSchemaFeeding
    milk_production: _CowSchemaMilkProduction
    has_calves: bool

    @validator("sex")
    def validate_sex(cls, v):
        valid_sex = ("Male", "Female")
        if v not in valid_sex:
            raise ValueError(f"{v} must be one of {valid_sex}")
        return v


class CowSchemaPost(CowSchemaBase):
    pass


class CowSchemaGet(CowSchemaBase):
    id: int

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row.id,
            name=row.name,
            sex=row.sex,
            birthdate=row.birthdate,
            condition=row.condition,
            has_calves=row.has_calves,
            feeding=_CowSchemaFeeding(
                amount_kg=row.feeding_amount_kg,
                cron_schedule=row.feeding_cron_schedule,
                last_measured=row.feeding_last_measured,
            ),
            weight=_CowSchemaWeight(
                mass_kg=row.weight_mass_kg,
                last_measured=row.weight_last_measured,
            ),
            milk_production=_CowSchemaMilkProduction(
                last_milk=row.milk_production_last_milk,
                cron_schedule=row.milk_production_cron_schedule,
                amount_l=row.milk_production_amount_l,
            ),
        )


class CowSchemaPut(BaseModel):
    id: int
    name: Optional[str]
    sex: Optional[str]
    birthdate: Optional[datetime]
    condition: Optional[str]
    weight: Optional[_CowSchemaWeight]
    feeding: Optional[_CowSchemaFeeding]
    milk_production: Optional[_CowSchemaMilkProduction]
