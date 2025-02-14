from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City:
    query = select(models.City).filter(models.City.id == city_id)
    city = await db.execute(query)
    return city.scalar()


async def get_city_by_name(db: AsyncSession, name: str) -> models.City:
    query = select(models.City).filter(models.City.name == name)
    city = await db.execute(query)
    return city.scalar()


async def create_city(
    db: AsyncSession, city: schemas.CityCreate
) -> models.City:
    query = insert(models.City).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def update_city(
    db: AsyncSession, city_id: int, updated_city: schemas.CityUpdate
) -> models.City:
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if db_city:
        query = (
            update(models.City)
            .where(models.City.id == city_id)
            .values(
                name=updated_city.name,
                additional_info=updated_city.additional_info,
            )
        )
        await db.execute(query)
        await db.commit()

        response = {**updated_city.model_dump(), "id": city_id}
        return response

    raise HTTPException(status_code=404, detail="City not found")


async def delete_city(db: AsyncSession, city_id: int) -> dict:
    db_city = await get_city_by_id(db=db, city_id=city_id)
    if db_city:
        query = delete(models.City).where(models.City.id == city_id)
        await db.execute(query)
        await db.commit()
        return {"message": "City deleted"}

    raise HTTPException(status_code=404, detail="City not found")
