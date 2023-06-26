from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import validator


class _Base(BaseModel):
    class Config:
        validate_assignment = True

    @validator("*")
    def remove_timezone(cls, value):
        # Removing timezones is so that openapi docs work.
        # A production implementation would handle timezones
        if isinstance(value, datetime):
            return value.replace(tzinfo=None)
        return value

    @classmethod
    def _flatten(cls, a: dict, prefix="") -> dict:
        res = {}
        for k, v in a.items():
            if isinstance(v, dict):
                nested = cls._flatten(v, prefix=f"{k}_")
                for fk, fv in nested.items():
                    res[fk] = fv
            else:
                res[f"{prefix}{k}"] = v
        return res

    def flatten(self) -> dict:
        return self._flatten(self.dict(exclude_unset=True))


class _Weight(_Base):
    mass_kg: int
    last_measured: datetime


class _MilkProduction(_Base):
    last_milk: datetime
    cron_schedule: str
    amount_l: int


class _Feeding(_Base):
    amount_kg: int
    cron_schedule: str
    last_measured: datetime


class Delete(_Base):
    id: int


class Base(_Base):
    name: str
    sex: str
    birthdate: datetime
    condition: str
    weight: _Weight
    feeding: _Feeding
    milk_production: _MilkProduction
    has_calves: bool

    @validator("sex")
    def validate_sex(cls, v):
        valid_sex = ("Male", "Female")
        if v not in valid_sex:
            raise ValueError(f"{v} must be one of {valid_sex}")
        return v


class Post(Base):
    pass


class Get(Base):
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
            feeding=_Feeding(
                amount_kg=row.feeding_amount_kg,
                cron_schedule=row.feeding_cron_schedule,
                last_measured=row.feeding_last_measured,
            ),
            weight=_Weight(
                mass_kg=row.weight_mass_kg,
                last_measured=row.weight_last_measured,
            ),
            milk_production=_MilkProduction(
                last_milk=row.milk_production_last_milk,
                cron_schedule=row.milk_production_cron_schedule,
                amount_l=row.milk_production_amount_l,
            ),
        )


class Put(_Base):
    # TODO PUT veresion of each nested schema
    name: Optional[str]
    sex: Optional[str]
    birthdate: Optional[datetime]
    condition: Optional[str]
    weight: Optional[_Weight]
    feeding: Optional[_Feeding]
    milk_production: Optional[_MilkProduction]
